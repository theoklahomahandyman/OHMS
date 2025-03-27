import { Modal, Button, Spinner } from 'react-bootstrap';
import { adminAPI } from '../../api';
import PropTypes from 'prop-types';
import { useState } from 'react'

export default function DeleteAdminModal({ show, onHide, admin, fetchData }) {
    const [loading, setLoading] = useState(false);

    const handleDelete = async () => {
        setLoading(true);
        try {
            await adminAPI.deleteAdmin(admin.id);
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
                Are you sure you want to delete {admin?.first_name} {admin?.last_name}?
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

DeleteAdminModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired,
    admin: PropTypes.object.isRequired,
    fetchData: PropTypes.func.isRequired,
};
