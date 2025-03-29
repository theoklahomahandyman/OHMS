import { Card, Table, Alert, Button, Container, Spinner } from 'react-bootstrap';
import CreateAdminModal from './CreateModal';
import DeleteAdminModal from './DeleteModal';
import UpdateAdminModal from './UpdateModal';
import { useState, useEffect } from 'react';
import { adminAPI } from '../../api';
import $ from 'jquery';

export default function AdminTable() {
    const [selectedAdmin, setSelectedAdmin] = useState(null);
    const [showCreate, setShowCreate] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [showUpdate, setShowUpdate] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState([]);

    const fields = [
        { name: 'first_name', label: 'First Name', type: 'text' },
        { name: 'last_name', label: 'Last Name', type: 'text' },
        { name: 'email', label: 'Email', type: 'email' },
        { name: 'phone', label: 'Phone Number', type: 'text' },
        { name: 'pay_rate', label: 'Pay Rate', type: 'number' },
        { name: 'is_active', label: 'Status', type: 'checkbox' },
    ];

    const fetchAdmins = async () => {
        try {
            setLoading(true);
            const response = await adminAPI.getAdmins();
            setData(response.data);
        } catch (error) {
            setError('Failed to load administrators');
            console.error('Admin fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAdmins();
    }, []);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0) {
            setTimeout(() => {
                $('#adminTable').DataTable();
            }, 1);
        }
    }, [data]);

    return (
        <Container fluid>
            <Card className='shadow mb-4'>
                <Card.Header className='py-3 d-flex justify-content-between align-items-center'>
                    <h5 className='m-0 font-weight-bold text-primary'>Administrators</h5>
                    <Button variant='primary' onClick={() => setShowCreate(true)}>Add Administrator</Button>
                </Card.Header>
                <Card.Body>
                    { error && <Alert variant='danger'>{ error }</Alert> }
                    { loading ? (
                        <div className='text-center'>
                            <Spinner animation='border' role='status'>
                                <span className='visually-hidden'>Loading...</span>
                            </Spinner>
                        </div>
                    ) : (
                        <Table responsive striped bordered hover id='adminTable'>
                            <thead>
                                <tr>
                                    { fields.map((field) => (
                                        <th key={field.name} className='text-center'>{ field.label }</th>
                                    ))}
                                    <th className='text-center' key='actions-header'>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                { data.length > 0 ? (
                                    data.map((admin) => (
                                        <tr key={admin.id} className='text-center'>
                                            {fields.map((field) => (
                                                <td key={`${field.name}-${admin.id}`}>
                                                    { field.name === 'is_active' ? (
                                                        <span style={{ color: admin[field.name] ? 'green' : 'red'}}>{ admin[field.name] ? 'Active' : 'Inactive' }</span>
                                                    ) : (
                                                        admin[field.name]
                                                    )}
                                                </td>
                                            ))}
                                            <td>
                                                <Button variant='info' size='sm' className='me-2'>Edit</Button>
                                                <Button variant='danger' size='sm' onClick={() => {setSelectedAdmin(admin); setShowDelete(true)}}>Delete</Button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={fields.length + 1} className='text-center'>
                                            { error ? 'Error loading data' : 'No administrators found' }
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    )}
                </Card.Body>
            </Card>
            <CreateAdminModal show={showCreate} onHide={() => setShowCreate(false)} fields={fields} fetchData={fetchAdmins} />
            <UpdateAdminModal show={showUpdate} onHide={() => setShowUpdate(false)} fields={fields} admin={selectedAdmin} fetchData={fetchAdmins} />
            <DeleteAdminModal show={showDelete} onHide={() => setShowDelete(false)} admin={selectedAdmin} fetchData={fetchAdmins} />
        </Container>
    );
};
