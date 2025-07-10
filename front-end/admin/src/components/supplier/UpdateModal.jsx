import SupplierForm from './SupplierForm';
import { Modal } from 'react-bootstrap';
import { supplierAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function UpdateModal({ supplier, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (formData, addresses) => {
        setLoading(true);
        try {
            const dataToSend = {
                id: supplier.id,
                ...formData,
                addresses: addresses.map(addr => ({
                    ...addr,
                    zip: addr.zip ? parseInt(addr.zip) : null
                })).filter(addr =>
                    addr.street_address || addr.city || addr.state || addr.zip || addr.notes
                )
            };
            await supplierAPI.updateSupplier(dataToSend);
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
                <Modal.Title>Edit Supplier</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <SupplierForm supplierData={supplier} onSubmit={handleSubmit} errors={errors} loading={loading} />
            </Modal.Body>
        </Modal>
    );
};

UpdateModal.propTypes = {
    supplier: PropTypes.object,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
