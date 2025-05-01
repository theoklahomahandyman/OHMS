import { Modal, Button, Spinner, Alert } from 'react-bootstrap';
import { useState, useEffect, useMemo } from 'react';
import { customerAPI } from '../../api';
import CustomerForm from './CustomerForm';
import PropTypes from 'prop-types';

export default function UpdateCustomerModal({ fields, customer, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [initialData, setInitialData] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (customer) {
            setFormData({ ...customer });
            setInitialData({ ...customer });
        }
    }, [customer]);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await customerAPI.updateCustomer({ ...formData });
            fetchData();
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
        } finally {
            setLoading(false);
        }
    };

    const isFormUnchanged = useMemo(() => {
        if (!initialData) return true;
        const currentPhone = (formData.phone || '').replace(/\D/g, '');
        const initialPhone = (initialData.phone || '').replace(/\D/g, '') || '';
        return (
            formData.first_name === initialData.first_name &&
            formData.last_name === initialData.last_name &&
            formData.email === initialData.email &&
            currentPhone === initialPhone &&
            formData.notes === initialData.notes
        );
    }, [formData, initialData]);

    return (
        <Modal show={show} onHide={onHide} size='lg'>
            <Modal.Header closeButton>
                <Modal.Title>Edit Customer</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { Object.keys(errors).length > 0 && (
                    <Alert variant='danger'>Please fix the form errors</Alert>
                )}
                <CustomerForm fields={fields} formData={formData} setFormData={setFormData} errors={errors} />
            </Modal.Body>
            <Modal.Footer className='p-3 d-flex justify-content-between'>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='primary' onClick={handleSubmit} disabled={loading || isFormUnchanged}>
                    { loading ? <Spinner size='sm' /> : 'Save Changes' }
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

UpdateCustomerModal.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool
    })).isRequired,
    customer: PropTypes.object,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
