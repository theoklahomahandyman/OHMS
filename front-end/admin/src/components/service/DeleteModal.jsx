import { Modal, Button, Spinner } from 'react-bootstrap';
import { serviceAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react'

export default function DeleteServiceModal({ show, onHide, service, fetchData }) {
    const [loading, setLoading] = useState(false);

    const handleDelete = async () => {
        setLoading(true);
        try {
            await serviceAPI.deleteService(service.id);
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
                Are you sure you want to delete {service?.first_name} {service?.last_name}?
            </Modal.Body>
            <Modal.Footer>
                <Button variant='secondary' onClick={onHide}>Cancel</Button>
                <Button variant='danger' onClick={handleDelete} disabled={loading}>
                    { loading ? <Spinner size='sm' /> : 'Delete' }
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

DeleteServiceModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    service: PropTypes.object.isRequired,
    fetchData: PropTypes.func.isRequired,
};
