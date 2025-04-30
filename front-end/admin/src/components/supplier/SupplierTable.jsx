import { Card, Table, Alert, Button, Container, Spinner } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { supplierAPI } from '../../api';
import CreateModal from './CreateModal';
import UpdateModal from './UpdateModal';
import DeleteModal from './DeleteModal';
import $ from 'jquery';

export default function SupplierTable() {
    const [selectedSupplier, setSelectedSupplier] = useState(null);
    const [showCreate, setShowCreate] = useState(false);
    const [showUpdate, setShowUpdate] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState({})

    const fields = [
        { name: 'name', label: 'Supplier Name' },
        { name: 'notes', label: 'Notes' }
    ];

    const fetchSuppliers = async () => {
        setLoading(true);
        try {
            const response = await supplierAPI.getSuppliers();
            setData(response);
        } catch (error) {
            setError('Failed to load suppliers');
            console.error('Supplier fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSuppliers();
    }, []);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0) {
            setTimeout(() => {
                $('#supplierTable').DataTable();
            }, 1);
        }
    }, [data]);

    return (
        <Container fluid>
            <Card className='shadow mb-4'>
                <Card.Header className='py d-flex justify-content-between align-items-center'>
                    <h5 className='m-0 font-weight-bold text-primary'>Suppliers</h5>
                    <Button variant='primary' onClick={() => setShowCreate(true)}>Add Supplier</Button>
                </Card.Header>
                <Card.Body>
                    {error && <Alert variant='danger'>{error}</Alert>}
                    {loading ? (
                        <div className='text-center'>
                            <Spinner animation='border' role='status'></Spinner><br />
                            <span className='visually-hidden'>Loading</span>
                        </div>
                    ) : (
                        <Table responsive striped bordered hover id='supplierTable' className='my-3'>
                            <thead>
                                <tr>
                                    {fields.map((field) => (
                                        <th key={field.name} className='text-center'>{field.label}</th>
                                    ))}
                                    <th className='text-center'>Locations</th>
                                    <th className='text-center' key='actions-header'>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                { Array.isArray(data) && data?.length > 0 ? data.map((supplier) => (
                                    <tr key={supplier.id} className='text-center'>
                                        {fields.map((field) => (
                                            <td key={`${field.name}-${supplier.id}`}>
                                                {supplier[field.name] || 'N/A'}
                                            </td>
                                        ))}
                                        <td>{supplier.addresses?.length || 0}</td>
                                        <td className='text-center' style={{ verticalAlign: 'middle', height: '75px' }}>
                                            <div className='d-flex justify-content-center'>
                                                <Button variant='info' size='sm' className='mr-2' onClick={() => { setSelectedSupplier(supplier); setShowUpdate(true) }}>Edit</Button>
                                                <Button variant='danger' size='sm' onClick={() => { setSelectedSupplier(supplier); setShowDelete(true) }}>Delete</Button>
                                            </div>
                                        </td>
                                    </tr>
                                )) : (
                                    <tr>
                                        <td colSpan={fields.length + 2} className='text-center'>
                                            {error ? 'Error loading data' : 'No suppliers found'}
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    )}
                </Card.Body>
            </Card>
            <CreateModal show={showCreate} onHide={() => setShowCreate(false)} fetchData={fetchSuppliers} />
            <UpdateModal show={showUpdate} onHide={() => setShowUpdate(false)} fetchData={fetchSuppliers} supplier={selectedSupplier} />
            <DeleteModal show={showDelete} onHide={() => setShowDelete(false)} fetchData={fetchSuppliers} supplier={selectedSupplier} />
        </Container>
    );
};
