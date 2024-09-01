import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';
import Modal from './Modal';
import Form from './Form';

function DeleteModal({ name, route, id, fetchData }) {
    const [visible, setVisible] = useState(false);

    const deleteRoute = `${route}${id}/`;

    const lowerName = name.toLowerCase();

    const handleSuccess = () => {
        fetchData();
        setVisible(false);
        toast.success(`${name} successfully deleted!`);
    }

    const handleError = () => {
        toast.error('An error occured so nothing was deleted. Please try again.');
    }


    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-danger action-btn'>Delete</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title={name}>
                <Form method='delete' route={deleteRoute} buttonText='Delete' buttonStyle='danger' onSuccess={handleSuccess} onError={handleError}>
                    <p className="text-center">Are you sure you want to delete this {lowerName}?</p>
                </Form>
            </Modal>
        </>
    )
}

DeleteModal.propTypes = {
    name: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    id: PropTypes.number.isRequired,
    fetchData: PropTypes.func.isRequired,
}

export default DeleteModal;
