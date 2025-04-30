import { Card, Table, Alert, Button, Container, Spinner } from 'react-bootstrap';
import CreateServiceModal from './CreateModal';
import UpdateServiceModal from './UpdateModal';
import DeleteServiceModal from './DeleteModal';
import { useState, useEffect } from 'react';
import { serviceAPI } from '../../api';
import $ from 'jquery';

export default function ServiceTable() {
    const [selectedService, setSelectedService] = useState(null);
    const [showCreate, setShowCreate] = useState(false);
    const [showUpdate, setShowUpdate] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState({});

    const fields = [
        {name: 'name', label: 'Service Name', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'description', label: 'Service Description', type: 'text', required: false, maxLength: 500, minLength: 0}
    ];

    const fetchServices = async () => {
        setLoading(true);
        try {
            const response = await serviceAPI.getServices();
            setData(response);
        } catch (error) {
            setError('Failed to load services');
            console.error('Service fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchServices();
    }, []);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0) {
            setTimeout(() => {
                $('#serviceTable').DataTable();
            }, 1);
        }
    }, [data]);

    return (
        <Container fluid>
            <Card className='shadow mb-4'>
                <Card.Header className='py-3 d-flex justify-content-between align-items-center'>
                    <h5 className='m-0 font-weight-bold text-primary'>Services</h5>
                    <Button variant='primary' onClick={() => setShowCreate(true)}>Add Service</Button>
                </Card.Header>
                <Card.Body>
                    { error && <Alert variant='danger'>{ error }</Alert>}
                    { loading ? (
                        <div className='text-center'>
                            <Spinner animation='border' role='status'></Spinner><br />
                            <span className='visually-hidden'>Loading...</span>
                        </div>
                    ) : (
                        <Table responsive striped bordered hover id='serviceTable' className='my-3'>
                            <thead>
                                <tr>
                                    { fields.map((field) => (
                                        <th key={field.name} className='text-center'>{ field.label }</th>
                                    ))}
                                    <th className='text-center' key='actions-header'>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                { data?.length > 0 ? data.map((service) => (
                                    <tr key={service.id} className='text-center'>
                                        { fields.map((field) => (
                                            <td key={`${field.name}-${service.id}`}>
                                                {service[field.name] || 'N/A'}
                                            </td>
                                        ))}
                                        <td>
                                            <Button variant='info' size='sm' className='me-2 mr-4' onClick={() => { setSelectedService(service); setShowUpdate(true) }}>Edit</Button>
                                            <Button variant='danger' size='sm' className='me-2' onClick={() => { setSelectedService(service); setShowDelete(true) }}>Delete</Button>
                                        </td>
                                    </tr>
                                )) : (
                                    <tr>
                                        <td colSpan={fields.length + 1} className='text-center'>
                                            {error ? 'Error loading data' : 'No services found'}
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    )}
                </Card.Body>
            </Card>
            <CreateServiceModal show={showCreate} onHide={() => setShowCreate(false)} fetchData={fetchServices} fields={fields} />
            <UpdateServiceModal show={showUpdate} onHide={() => setShowUpdate(false)} fetchData={fetchServices} fields={fields} service={selectedService} />
            <DeleteServiceModal show={showDelete} onHide={() => setShowDelete(false)} fetchData={fetchServices} service={selectedService} />
        </Container>
    );
};
