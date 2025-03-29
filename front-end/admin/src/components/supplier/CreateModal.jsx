import SupplierForm from './SupplierForm';
import { supplierAPI } from '../../api';
import { Modal } from 'react-bootstrap';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateModal({ show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (formData) => {
        setLoading(true);
        try {
            const { data: supplier } = await supplierAPI.createSupplier({
                name: formData.name,
                notes: formData.notes
            });
            await Promise.all(formData.addresses.map(address =>
                supplierAPI.createAddress(supplier.id, address)
            ));
            fetchData();
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal show={show} onHide={onHide} size='xl'>
            <Modal.Header closeButton>
                <Modal.Title>Create New Supplier</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <SupplierForm onSubmit={handleSubmit} errors={errors} loading={loading} />
            </Modal.Body>
        </Modal>
    );
};

CreateModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
