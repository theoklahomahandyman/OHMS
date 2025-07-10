import SupplierForm from './SupplierForm';
import { supplierAPI } from '../../api';
import { Modal } from 'react-bootstrap';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateModal({ show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (formData, addresses) => {
        setLoading(true);
        try {
            const dataToSend = {
                ...formData,
                addresses: addresses.map(addr => ({
                    ...addr,
                    zip: addr.zip ? parseInt(addr.zip) : null
                })).filter(addr =>
                    addr.street_address || addr.city || addr.state || addr.zip || addr.notes
                )
            };
            const response = await supplierAPI.createSupplier(dataToSend);
            console.log(response)
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
