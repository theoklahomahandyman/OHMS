import { Modal, Spinner } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import PurchaseForm from './PurchaseForm';
import { purchaseAPI } from '../../api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';

export default function UpdateModal({ purchase, show, onHide, fetchData }) {
    const [initialData, setInititalData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    useEffect(() => {
        const fetchPurchaseDetails = async () => {
            if (purchase) {
                try {
                    const [materialRes, toolRes] = await Promise.all([
                        purchaseAPI.getMaterials(purchase.id),
                        purchaseAPI.getTools(purchase.id),
                    ]);
                    setInititalData({
                        ...purchase,
                        materials: materialRes.data,
                        tools: toolRes.data
                    });
                } catch (error) {
                    toast.error('Failed to load purchase details');
                    console.error('Error fetching purchase details:', error);
                }
            }
        };
        fetchPurchaseDetails();
    }, [purchase]);

    const handleSubmit = async (formData) => {
        setLoading(true);
        setErrors({});
        try {
            await purchaseAPI.updatePurchase(purchase.id, {
                supplier: formData.supplier,
                supplier_address: formData.supplier_address,
                date: formData.date,
                tax: formData.tax,
            });
            const materialUpdates = formData.materials.map(material => {
                if (material.id) {
                    return purchaseAPI.updateMaterial(purchase.id, material.id, {
                        inventory_item: material.inventory_item,
                        quantity: material.quantity,
                        cost: material.cost
                    });
                }
                return purchaseAPI.addMaterial(purchase.id, {
                    inventory_item: material.inventory_item,
                    quantity: material.quantity,
                    cost: material.cost
                });
            });
            await Promise.all(materialUpdates);
            const toolUpdates = formData.tools.map(tool => {
                if (tool.id) {
                    return purchaseAPI.updateTool(purchase.id, tool.id, {
                        inventory_item: tool.inventory_item,
                        quantity: tool.quantity,
                        cost: tool.cost
                    });
                }
                return purchaseAPI.addTool(purchase.id, {
                    inventory_item: tool.inventory_item,
                    quantity: tool.quantity,
                    cost: tool.cost
                });
            });
            await Promise.all(toolUpdates);
            if (formData.uploaded_images?.length > 0) {
                await Promise.all(formData.uploaded_images.map(file => {
                    const formData = new FormData();
                    formData.append('image', file);
                    return purchaseAPI.addReceipt(purchase.id, formData)
                }));
            }
            toast.success('Purchase updated successfully!');
            fetchData();
            onHide();
        } catch (error) {
            console.error('Purchase update error:', error);
            if (error.response?.data) {
                setErrors(error.response.data);
                toast.error('Failed to update purchase - check form errors');
            } else {
                toast.error('Failed to update purchase - please try again');
            }
        }
    };

    return (
        <Modal show={show} onHide={onHide} size='xl' centered>
            <Modal.Header closeButton className='bg-light'>
                <Modal.Title>Edit Purchase PUR-{purchase?.id}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { initialData ? (
                    <PurchaseForm initialData={initialData} onSubmit={handleSubmit} errors={errors} loading={loading} />
                ) : (
                    <div className='text-center'>
                        <Spinner animation='border' />
                        <p>Loading purchase details...</p>
                    </div>
                )}
            </Modal.Body>
        </Modal>
    );
};

UpdateModal.propTypes = {
    purchase: PropTypes.shape({
        id: PropTypes.number.isRequired,
        supplier: PropTypes.number.isRequired,
        supplier_address: PropTypes.number.isRequired,
        date: PropTypes.string.isRequired,
        tax: PropTypes.number.isRequired
    }).isRequired,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
