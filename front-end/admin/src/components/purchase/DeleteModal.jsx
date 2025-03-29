import { Modal, Button, Spinner } from 'react-bootstrap';
import { purchaseAPI } from '../../api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function DeleteModal({ purchase, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);

    const handleDelete = async () => {
        setLoading(true);
        try {
            await purchaseAPI.deletePurchase(purchase.id);
            toast.success('Purchase deleted successfully');
            fetchData();
            onHide();
        } catch (error) {
            console.error('Delete purchase errr:', error);
            toast.error('Failed to delete purchase - please try again');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal show={show} onHide={onHide} centered>
            <Modal.Header closeButton>
                <Modal.Title>Confirm Delete</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                Are you sure you want to delete purchase PUR-{purchase?.id}?
                <br />
                <strong>Supplier:</strong> {purchase?.supplier?.name}
                <br />
                <strong>Date:</strong> {new Date(purchase?.date).toLocaleDateString()}
                <br />
                <strong>Total:</strong> ${purchase?.total?.toFixed(2)}
            </Modal.Body>
            <Modal.Footer>
                <Button variant='secondary' onCliick={onHide} disabled={loading}>Cancel</Button>
                <Button variant='danger' onClick={handleDelete} disabled={loading}>
                    {loading ? (
                        <Spinner animation='border' size='sm' />
                    ) : 'Delete Purchase'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

DeleteModal.propTypes = {
    purchase: PropTypes.shapt({
        id: PropTypes.number.isRequired,
        supplier: PropTypes.object.isRequired,
        date: PropTypes.string.isRequired,
        total: PropTypes.number.isRequired
    }).isRequired,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
