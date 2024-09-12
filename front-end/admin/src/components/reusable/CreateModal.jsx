import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';
import Modal from './Modal';
import Form from './Form';

function CreateModal({ name, fields, route, fetchData }) {
    const [visible, setVisible] = useState(false);

    const handleSuccess = () => {
        fetchData();
        toast.success(`${name} successfully created!`);
        setVisible(false);
    }

    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-success action-btn'>Create</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title={name}>
                <Form method='post' route={route} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} />
            </Modal>
        </>
    )
}

CreateModal.propTypes = {
    name: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    fetchData: PropTypes.func.isRequired,
    fields: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            type: PropTypes.string,
            required: PropTypes.bool.isRequired,
            elementType: PropTypes.string.isRequired,
            maxLength: PropTypes.number,
            minLength: PropTypes.number,
            accept: PropTypes.string,
            multiple: PropTypes.bool,
            data: PropTypes.arrayOf(PropTypes.shape({
                value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
                label: PropTypes.string.isRequired
            })),
            customChange: PropTypes.func,
        })
    ).isRequired,
}

export default CreateModal;
