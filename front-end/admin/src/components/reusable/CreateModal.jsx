import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';
import Modal from './Modal';
import Form from './Form';

function CreateModal({ name, fields, route, fetchData }) {
    const [visible, setVisible] = useState(false);
    const [errors, setErrors] = useState({});
    const [data, setData] = useState({});

    const handleSuccess = () => {
        fetchData();
        toast.success(`${name} successfully created!`);
        setVisible(false);
        setData({});
        setErrors({});
    }

    const handleError = (data) => {
        const formattedErrors = {};
        if (typeof data === 'object' && !Array.isArray(data)) {
            for (let fieldName in data) {
                if (Object.prototype.hasOwnProperty.call(data, fieldName)) {
                    const array = data[fieldName];
                    if (Array.isArray(array)) {
                        formattedErrors[fieldName] = array;
                    } else if (typeof array === 'string') {
                        formattedErrors[fieldName] = [array];
                    } else {
                        formattedErrors[fieldName] = ['Unknown error'];
                    }
                }
            }
        }
        setErrors(formattedErrors);
    }


    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-success action-btn'>Create</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title={name}>
                <Form method='post' route={route} data={data} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} onError={handleError} setErrors={setErrors} fields={fields} setData={setData} errors={errors} />
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
            type: PropTypes.string.isRequired,
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
        })
    ).isRequired,
}

export default CreateModal;
