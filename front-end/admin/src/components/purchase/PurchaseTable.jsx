import { Card, Table, Alert, Button, Container, Spinner } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import CreateModal from './CreateModal';
import UpdateModal from './UpdateModal';
import DeleteModal from './DeleteModal';
import { purchaseAPI } from '../../api';
import $ from 'jquery';

export default function PurchaseTable() {
    const [selectedPurchase, setSelectedPurchase] = useState(null);
    const [showCreate, setShowCreate] = useState(false);
    const [showUpdate, setShowUpdate] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [data, setData] = useState([]);

    const fetchPurchases = async () => {
        setLoading(true);
        try {
            const response = await purchaseAPI.getPurchases();
            setData(response.data);
        } catch (error) {
            setError('Failed to load purchases');
            console.error('Purchase fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPurchases();
    }, []);


    useEffect(() => {
        if (data.length > 0) {
            setTimeout(() => $('#purchaseTable').DataTable(), 1);
        }
    }, [data]);

    return (
        <Container fluid>
            <Card className='shadow mb-4'>
                <Card.Header className='py-3 d-flex justify-content-between align-items-center'>
                    <h5 className='m-0 font-weight-bold text-primary'>Purchases</h5>
                    <Button variant='primary' onClick={() => setShowCreate(true)}>New Purchase</Button>
                </Card.Header>
                <Card.Body>
                    {error && <Alert variant='danger'>{error}</Alert>}
                    {loading ? (
                        <div className='text-center'>
                            <Spinner animation='border' />
                        </div>
                    ) : (
                        <Table responsive striped bordered hover id='purchaseTable'>
                            <thead>
                                <tr>
                                    <th>Purchase ID</th>
                                    <th>Supplier</th>
                                    <th>Total</th>
                                    <th>Date</th>
                                    <th>Materials</th>
                                    <th>Tools</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.map(purchase => (
                                    <tr key={purchase.id}>
                                        <td>PUR-{purchase.id}</td>
                                        <td>{purchase.supplier?.name}</td>
                                        <td>${purchase.total}</td>
                                        <td>{new Date(purchase.date).toLocaleDateString()}</td>
                                        <td>{purchase.materials?.length || 0}</td>
                                        <td>{purchase.tools?.length || 0}</td>
                                        <td>
                                            <Button variant='info' size='sm' onClick={() => {setSelectedPurchase(purchase); setShowUpdate(true)}}>Edit</Button>
                                            <Button variant='danger' size='sm' className='ms-2' onClick={() => {setSelectedPurchase(purchase); setShowDelete(true)}}>Delete</Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    )}
                </Card.Body>
            </Card>
            <CreateModal show={showCreate} onHide={() => setShowCreate(false)} fetchData={fetchPurchases} />
            <UpdateModal show={showUpdate} onHide={() => setShowUpdate(false)} fetchData={fetchPurchases} purchase={selectedPurchase} />
            <DeleteModal show={showDelete} onHide={() => setShowDelete(false)} fetchData={fetchPurchases} purchase={selectedPurchase} />
        </Container>
    );
};
