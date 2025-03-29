import { Modal, Button, Spinner, Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import ServiceForm from './ServiceForm';
import { serviceAPI } from '../../api';
import PropTypes from 'prop-types';

export default function UpdateServiceModal({ fields, service, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (service) setFormData({ ...service });
    }, [service]);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await serviceAPI.updateService({ ...formData });
            fetchData();
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    return (
        <Modal show={show} onHide={onHide} size='lg'>
            <Modal.Header closeButton>
                <Modal.Title>Edit Service</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { Object.keys(errors).length > 0 && (
                    <Alert variant='danger'>Please fix the form errors</Alert>
                )}
                <ServiceForm fields={fields} formData={formData} errors={errors} handleChange={handleChange} />
            </Modal.Body>
            <Modal.Footer>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='primary' onClick={handleSubmit} disabled={loading}>
                    { loading ? <Spinner size='sm' /> : 'Save Changes' }
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

UpdateServiceModal.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool
    })).isRequired,
    service: PropTypes.object.isRequired,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
