import { Modal, Button, Spinner, Alert } from 'react-bootstrap';
import CustomerForm from './CustomerForm';
import { customerAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreateCustomerModal({ fields, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await customerAPI.createCustomer(formData);
            fetchData();
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal show={show} onHide={onHide} size='lg'>
            <Modal.Header closeButton>
                <Modal.Title>Create New Customer</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { Object.keys(errors).length > 0 && <Alert variant='danger'>Please fix form errors</Alert> }
                <CustomerForm fields={fields} formData={formData} setFormData={setFormData} errors={errors} />
            </Modal.Body>
            <Modal.Footer className='p-3 d-flex justify-content-between'>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='primary' onClick={handleSubmit} disabled={loading}>
                    { loading ? <Spinner size='sm' /> : 'Create' }
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

CreateCustomerModal.propTypes = {
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
