import { Tab, Nav, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

export default function SupplierForm({ initialData, onSubmit, errors, loading }) {
    const [activeTab, setActiveTab] = useState('basic');
    const [formData, setFormData] = useState(initialData || {});
    const [addresses, setAddresses] = useState(initialData?.addresses || []);

    const locationFields = [
        { name: 'street_address', label: 'Street Address', type: 'text', required: true },
        { name: 'city', label: 'City', type: 'text', required: true },
        { name: 'state', label: 'State', type: 'text', required: true },
        { name: 'zip', label: 'Zip Code', type: 'text', required: true },
        { name: 'notes', label: 'Notes', type: 'text' }
    ];

    useEffect(() => {
        if (initialData) {
            setFormData(initialData);
            setAddresses(initialData.addresses || []);
        }
    }, [initialData]);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ ...formData, addresses });
    };

    const handleAddressChange = (index, field, value) => {
        const updatedAddresses = [...addresses];
        updatedAddresses[index] = { ...updatedAddresses[index], [field]: value };
        setAddresses(updatedAddresses);
    };

    const addAddress = () => {
        setAddresses([...addresses, {}]);
    };

    const removeAddress = (index) => {
        const updatedAddresses = addresses.filter((_, i) => i !== index);
        setAddresses(updatedAddresses);
    };

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
                            <Form.Control type='text' reqired
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
                        <div className='text-end'>
                            <Button variant='primary' onClick={() => setActiveTab('locations')}>Next</Button>
                        </div>
                    </Tab.Pane>
                    <Tab.Pane eventKey='locations'>
                        {addresses.map((address, index) => (
                            <div key={index} className='border p-3 mb-3'>
                                <div className='d-flex justify-content-between mb-2'>
                                    <h6>Location {index + 1}</h6>
                                    <Button variant='danger' size='sm' onClick={() => removeAddress(index)}>Remove</Button>
                                </div>
                                {locationFields.map((field) => (
                                    <Form.Group key={field.name} className='mb-3'>
                                        <Form.Label>{field.label}</Form.Label>
                                        <Form.Control type={field.type} required={field.required}
                                            value={address[field.name] || ''}
                                            onChange={(e) => handleAddressChange(index, field.name, e.target.value)}
                                            isInvalid={!!errors[`addresses.${index}.${field.name}`]}
                                        />
                                        <Form.Control.Feedback type='invalid'>
                                            {errors[`addresses.${index}.${field.name}`]?.join(' ')}
                                        </Form.Control.Feedback>
                                    </Form.Group>
                                ))}
                            </div>
                        ))}
                        <Button variant='success' onClick={addAddress} className='mb-3'>Add Location</Button>
                        <div className='d-flex justify-content-between'>
                            <Button variant='secondary' onClick={() => setActiveTab('basic')}>Back</Button>
                        </div>
                    </Tab.Pane>
                </Tab.Content>
            </Tab.Container>
            {Object.keys(errors).length > 0 && (
                <Alert variant='danger' className='mt-3'>
                    Please fix form errors
                </Alert>
            )}
            <div className='text-end mt-4'>
                <Button variant='primary' type='submit' disabled={loading}>
                    {loading ? (
                        <Spinner animation='border' size='sm' />
                    ) : initialData ? 'Save Changes' : 'Create Supplier'}
                </Button>
            </div>
        </Form>
    );
};

SupplierForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    errors: PropTypes.object.isRequired,
    loading: PropTypes.bool.isRequired,
    initialData: PropTypes.objectOf(PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        notes: PropTypes.string,
        locations: PropTypes.arrayOf(PropTypes.shape({
            street_address: PropTypes.string,
            city: PropTypes.string,
            state: PropTypes.string,
            zip: PropTypes.string,
            notes: PropTypes.string
        }))
    }))
};
