import { Modal, Button, Spinner, Alert } from 'react-bootstrap';
import ServiceForm from './ServiceForm';
import { toast } from 'react-toastify';
import { serviceAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateServiceModal({ fields, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await serviceAPI.createService(formData);
            setFormData({});
            fetchData();
            toast.success('Service successfully created!');
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
            <Modal.Footer className='p-3 d-flex justify-content-center align-items-center'>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button type='button' variant='primary' onClick={handleSubmit} disabled={loading}>
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
