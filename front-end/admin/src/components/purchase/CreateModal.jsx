import PurchaseForm from './PurchaseForm';
import { Modal } from 'react-bootstrap';
import { purchaseAPI } from '../../api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateModal({ show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (formData) => {
        setLoading(true);
        setErrors({});
        try {
            const { data: createdPurchase } = await purchaseAPI.createPurchase({
                supplier: formData.supplier,
                supplier_address: formData.supplier_address,
                date: formData.date,
                tax: formData.tax
            });
            await Promise.all(formData.materials.map(material =>
                purchaseAPI.addMaterial(createdPurchase.id, {
                    inventory_item: material.inventory_item,
                    quantity: material.quantity,
                    cost: material.cost
                })
            ));
            await Promise.all(formData.newMaterials.map(material =>
                purchaseAPI.addNewMaterial(createdPurchase.id, {
                    name: material.name,
                    description: material.description,
                    size: material.size,
                    quantity: material.quantity,
                    cost: material.cost
                })
            ));
            await Promise.all(formData.tools.map(tool =>
                purchaseAPI.addTool(createdPurchase.id, {
                    inventory_item: tool.inventory_item,
                    quantity: tool.quantity,
                    cost: tool.cost
                })
            ));
            await Promise.all(formData.newTools.map(tool =>
                purchaseAPI.addNewTool(createdPurchase.id, {
                    name: tool.name,
                    description: tool.description,
                    quantity: tool.quantity,
                    cost: tool.cost
                })
            ));
            if (formData.uploaded_images?.length > 0) {
                await Promise.all(formData.uploaded_images.map(file => {
                    const formData = new FormData();
                    formData.append('image', file);
                    return purchaseAPI.addReceipt(createdPurchase.id, formData);
                }));
            }
            toast.success('Purchase created successfully!');
            fetchData();
            onHide();
        } catch (error) {
            console.error('Purchase creation error:', error);
            if (error.response?.data) {
                setErrors(error.response.data);
                toast.error('Failed to create purchase - check form errors');
            } else {
                toast.error('Failed to create purchase - please try again');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal show={show} onHide={onHide} size='xl' centered>
            <Modal.Header closeButton className='bg-light'>
                <Modal.Title>Create New Purchase</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <PurchaseForm onSubmit={handleSubmit} errors={errors} loading={loading} />
            </Modal.Body>
        </Modal>
    );
};

CreateModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
