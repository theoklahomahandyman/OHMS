import { Tab, Nav, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useState, useEffect, useMemo } from 'react';
import PropTypes from 'prop-types';

export default function SupplierForm({ supplierData, onSubmit, errors, loading }) {
    const [activeTab, setActiveTab] = useState('basic');
    const [formData, setFormData] = useState({});
    const [initialData, setInitialData] = useState({});
    const [addresses, setAddresses] = useState([]);
    const [initialAddresses, setInitialAddresses] = useState([]);

    const emptyAddress = useMemo(() => ({
        street_address: '',
        city: '',
        state: '',
        zip: '',
        notes: ''
    }), []);

    useEffect(() => {
        if (supplierData) {
            setFormData({ ...supplierData });
            setInitialData({ ...supplierData });
            setAddresses([ ...(supplierData?.addresses || []) ]);
            setInitialAddresses([ ...(supplierData?.addresses || []) ]);
        } else {
            setFormData({ name: '', notes: '' });
            setAddresses([ emptyAddress ]);
        }
    }, [supplierData, emptyAddress]);

    const locationFields = [
        { name: 'street_address', label: 'Street Address', type: 'text', required: true },
        { name: 'city', label: 'City', type: 'text', required: true },
        { name: 'state', label: 'State', type: 'text', required: true },
        { name: 'zip', label: 'Zip Code', type: 'text', required: true },
        { name: 'notes', label: 'Notes', type: 'text' }
    ];

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData, addresses);
        console.log(errors);
    };

    const handleAddressChange = (index, field, value) => {
        const updatedAddresses = [...addresses];
        updatedAddresses[index] = { ...updatedAddresses[index], [field]: value };
        setAddresses(updatedAddresses);
    };

    const addAddress = () => {
        setAddresses([...addresses, emptyAddress]);
    };

    const removeAddress = (index) => {
        const updatedAddresses = addresses.filter((_, i) => i !== index);
        setAddresses(updatedAddresses);
    };

    const isFormUnchanged = useMemo(() => {
            if (!initialData && !supplierData) return false;
            const baseUnchanged = formData.name === initialData.name && formData.notes === initialData.notes;
            const addressesUnchanged = JSON.stringify(addresses) === JSON.stringify(initialAddresses);
            return (
                baseUnchanged,
                addressesUnchanged
            );
        }, [formData, initialData, addresses, initialAddresses, supplierData]);


    return (
        <Form onSubmit={handleSubmit}>
            <Tab.Container activeKey={activeTab}>
                <Nav variant='tabs' className='mb-4'>
                    <Nav.Item>
                        <Nav.Link eventKey='basic' onClick={() => setActiveTab('basic')}>
                            Basic Info
                        </Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey='locations' onClick={() => setActiveTab('locations')}>
                            Locations ({addresses.length})
                        </Nav.Link>
                    </Nav.Item>
                </Nav>
                <Tab.Content>
                    <Tab.Pane eventKey='basic'>
                        <Form.Group className='mb-3'>
                            <Form.Label>Supplier Name</Form.Label>
                            <Form.Control type='text' required
                                value={formData.name || ''}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                isInvalid={!!errors.name}
                            />
                            <Form.Control.Feedback type='invalid'>
                                {errors.name?.join(' ')}
                            </Form.Control.Feedback>
                        </Form.Group>
                        <Form.Group className='mb-3'>
                            <Form.Label>Supplier Notes</Form.Label>
                            <Form.Control as='textarea' rows={3}
                                value={formData.notes || ''}
                                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                                isInvalid={!!errors.notes}
                            />
                        </Form.Group>
                        <div className='d-flex justify-content-end'>
                            <Button variant='primary' onClick={() => setActiveTab('locations')}>Next</Button>
                        </div>
                    </Tab.Pane>
                    <Tab.Pane eventKey='locations'>
                        {Array.isArray(addresses) && addresses.length > 0 ? addresses.map((address, index) => (
                            <div key={index} className='border p-3 mb-3'>
                                <div className='d-flex justify-content-between mb-2'>
                                    <h6>Location {index + 1}</h6>
                                    <Button variant='danger' size='sm' onClick={() => removeAddress(index)}>Remove</Button>
                                </div>
                                {locationFields.map((field) => (
                                    <Form.Group key={field.name} className='mb-3'>
                                        <Form.Label>{field.label}</Form.Label>
                                        <Form.Control type={field.type} required={field.required}
                                            value={address?.[field.name] || ''}
                                            onChange={(e) => handleAddressChange(index, field.name, e.target.value)}
                                            isInvalid={!!errors[`addresses.${index}.${field.name}`]}
                                        />
                                        <Form.Control.Feedback type='invalid'>
                                            {errors[`addresses.${index}.${field.name}`]?.join(' ')}
                                        </Form.Control.Feedback>
                                    </Form.Group>
                                ))}
                            </div>
                        )) : null}
                        <div className="d-flex justify-content-center">
                            <Button variant='success' onClick={addAddress} className='mb-3'>Add Location</Button>
                        </div>
                        <div className='d-flex justify-content-between'>
                            <Button variant='secondary' onClick={() => setActiveTab('basic')}>Back</Button>
                            <Button variant='primary' type='submit' disabled={loading || isFormUnchanged}>
                                {loading ? (
                                    <Spinner animation='border' size='sm' />
                                ) : initialData ? 'Save Changes' : 'Create Supplier'}
                            </Button>
                        </div>

                    </Tab.Pane>
                </Tab.Content>
            </Tab.Container>
            {Object.keys(errors).length > 0 && (
                <Alert variant='danger' className='mt-3'>
                    Please fix form errors
                </Alert>
            )}
        </Form>
    );
};

SupplierForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    errors: PropTypes.object.isRequired,
    loading: PropTypes.bool.isRequired,
    supplierData: PropTypes.object
};
