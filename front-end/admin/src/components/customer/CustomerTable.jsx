import { Card, Table, Alert, Button, Container, Spinner } from 'react-bootstrap';
import CreateCustomerModal from './CreateModal';
import UpdateCustomerModal from './UpdateModal';
import DeleteCustomerModal from './DeleteModal';
import { useState, useEffect } from 'react';
import { customerAPI } from '../../api';

export default function CustomerTable() {
    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [showCreate, setShowCreate] = useState(false);
    const [showUpdate, setShowUpdate] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState({});

    const fields = [
        {name: 'first_name', label: 'First Name', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'last_name', label: 'Last Name', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'email', label: 'Email', type: 'email', required: true, maxLength: 255, minLength: 8},
        {name: 'phone', label: 'Phone Number', type: 'text', required: true, maxLength: 17, minLength: 16},
        {name: 'notes', label: 'Customer Notes', type: 'text', required: false, maxLength: 500}
    ];

    const fetchCustomers = async () => {
        setLoading(true);
        try {
            const response = await customerAPI.getCustomers();
            setData(response.data);
        } catch (error) {
            setError('Failed to load customers');
            console.error('Customer fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCustomers();
    }, []);

    return (
        <Container fluid>
            <Card className='shadow mb-4'>
                <Card.Header className='py-3 d-flex jusify-content-between align-items-center'>
                    <h5 className='m-0 font-weight-bold text-primary'>Customers</h5>
                    <Button variant='primary' onClick={() => setShowCreate(true)}>Add Customer</Button>
                </Card.Header>
                <Card.Body>
                    { error && <Alert variant='danger'>{ error }</Alert>}
                    { loading ? (
                        <div className='text-center'>
                            <Spinner animation='border' role='status'>
                                <span className='visually-hidden'>Loading...</span>
                            </Spinner>
                        </div>
                    ) : (
                        <Table responsive striped bordered hover>
                            <thead>
                                <tr>
                                    { fields.map((field) => (
                                        <th key={field.name} className='text-center'>{ field.label }</th>
                                    ))}
                                    <th className='text-center' key='actions-header'>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                { data.length > 0 ? data.map((customer) => (
                                    <tr key={customer.id} className='text-center'>
                                        { fields.map((field) => (
                                            <td key={`${field.name}-${customer.id}`}>
                                                {customer[field.name] || 'N/A'}
                                            </td>
                                        ))}
                                        <td>
                                            <Button variant='info' size='sm' className='me-2' onClick={() => { setSelectedCustomer(customer); setShowUpdate(true)} }>Edit</Button>
                                            <Button variant='danger' size='sm' className='me-2' onClick={() => { setSelectedCustomer(customer); setShowDelete(true)} }>Delete</Button>
                                        </td>
                                    </tr>
                                )) : (
                                    <tr>
                                        <td colSpan={fields.length + 1} className='text-center'>
                                            {error ? 'Error loading data' : 'No customers found'}
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    )}
                </Card.Body>
            </Card>
            <CreateCustomerModal show={showCreate} onHide={() => setShowCreate(false)} fetchData={fetchCustomers} fields={fields} />
            <UpdateCustomerModal show={showUpdate} onHide={() => setShowUpdate(false)} fetchData={fetchCustomers} fields={fields} customer={selectedCustomer} />
            <DeleteCustomerModal show={showDelete} onHide={() => setShowDelete(false)} fetchData={fetchCustomers} customer={selectedCustomer} />
        </Container>
    );
};
