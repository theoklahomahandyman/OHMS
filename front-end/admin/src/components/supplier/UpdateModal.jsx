import { useState, useEffect } from 'react';
import SupplierForm from './SupplierForm';
import { Modal } from 'react-bootstrap';
import { supplierAPI } from '../../api';
import PropTypes from 'prop-types';

export default function UpdateModal({ supplier, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (formData) => {
        setLoading(true);
        try {
            await supplierAPI.updateSupplier(supplier.id, {
                name: formData.name,
                notes: formData.notes
            });
            await Promise.all(formData.addresses.map(address => {
                if (address.id) {
                    return supplierAPI.updateAddress(supplier.id, address.id, address);
                }
                return supplierAPI.createAddress(supplier.id, address);
            }));
            fetchData();
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const fetchAddresses = async () => {
            setLoading(true);
            try {
                supplier.addresses = await supplierAPI.getAddresses(supplier.id);
            } catch (error) {
                console.error('Error fetching supplier addresses:', error);
            } finally {
                setLoading(false);
            }
        }
        fetchAddresses();
    }, [supplier]);

    return (
        <Modal show={show} onHide={onHide} size='xl'>
            <Modal.Header closeButton>
                <Modal.Title>Edit Supplier</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <SupplierForm initialData={supplier} onSubmit={handleSubmit} errors={errors} loading={loading} />
            </Modal.Body>
        </Modal>
    );
};

UpdateModal.propTypes = {
    supplier: PropTypes.objectOf(PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        notes: PropTypes.string,
        locations: PropTypes.arrayOf(PropTypes.shape({
            street_address: PropTypes.string,
            city: PropTypes.string,
            state: PropTypes.string,
            zip: PropTypes.string,
            notes: PropTypes.string
        }))
    })).isRequired,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
