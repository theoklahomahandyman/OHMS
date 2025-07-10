import { Modal, Button, Spinner } from 'react-bootstrap';
import { supplierAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function DeleteModal({ supplier, show, onHide, fetchData }) {
    const [loading, setLoading] = useState(false);

    const handleDelete = async () => {
        setLoading(true);
        try {
            await supplierAPI.deleteSupplier(supplier.id);
            fetchData();
            onHide();
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
                Are you sure you want to delete {supplier?.name}?
            </Modal.Body>
            <Modal.Footer>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='danger' onClick={handleDelete} disabled={loading}>
                    {loading ? <Spinner size='sm' /> : 'Delete'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

DeleteModal.propTypes = {
    supplier: PropTypes.object,
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
};
