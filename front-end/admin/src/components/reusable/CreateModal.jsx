import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';
import Modal from './Modal';
import Input from './Input';
import Form from './Form';

function CreateModal({ name, fields, route }) {
    const [visible, setVisible] = useState(false);
    const [errors, setErrors] = useState({});
    const [data, setData] = useState({});

    const handleSuccess = (data) => {
        console.log(data)
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
            <Modal visible={visible} onClose={() => setVisible(false)}>
                <Form method='post' route={route} data={data} title={name} onSuccess={handleSuccess} onError={handleError} setErrors={setErrors}>
                    {fields.map((field, index) => {
                        return (<Input key={index} id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} accept={field.accept} multiple={field.multiple} error={errors[field.name]} />)
                    })}
                </Form>
            </Modal>
        </>
    )
}

CreateModal.propTypes = {
    name: PropTypes.string.isRequired,
    fields: PropTypes.array.isRequired,
    route: PropTypes.string.isRequired,
}

export default CreateModal;
