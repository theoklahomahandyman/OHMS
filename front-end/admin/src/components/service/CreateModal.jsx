import { Modal, Button, Spinner, Alert } from 'react-bootstrap';
import ServiceForm from './ServiceForm';
import { customerAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateServiceModal({ fields, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await customerAPI.createService(formData);
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
                <Modal.Title>Create New Service</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { Object.keys(errors).length > 0 && <Alert variant='danger'>Please fix form errors</Alert> }
                <ServiceForm fields={fields} formData={formData} errors={errors} handleChange={handleChange} />
            </Modal.Body>
            <Modal.Footer>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='primary' onClick={handleSubmit} disabled={loading}>
                    { loading ? <Spinner size='sm' /> : 'Create' }
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

CreateServiceModal.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool,
        maxLength: PropTypes.number,
        minLength: PropTypes.number
    })).isRequired,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
