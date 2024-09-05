import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import Loading from './Loading';
import Select from './Select';
import Input from './Input';
import api from '../../api';

function SubForm ({ fields, route, initialData, onSuccess, isNew }) {
    const [data, setData] = useState(initialData || {});
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [editing, setEditing] = useState(false);

    const formId = `subform-${Math.random().toString(36).substr(2, 9)}`;

    useEffect(() => {
        if (!isNew) {
            setEditing(false);
        }
    }, [isNew])

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            if (isNew){
                const response = await api.post(route, data);
                onSuccess(response.data)
            } else if (editing) {
                const response = await api.patch(route, data);
                onSuccess(response.data)
            }
        } catch (error) {
            if (error.response && error.response.data) {
                if (setErrors) {
                    handleError(error.response.data, setErrors);
                } else {
                    handleError(error.response.data)
                }
            } else {
                handleError({ non_field_errors: ['An unexpected error occured.']}, setErrors);
            }
        } finally {
            setLoading(false);
        }
    }

    const handleDelete = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await api.delete(route);
        onSuccess(response)
        } catch {
            toast.error('An error occurred so nothing was deleted. Please try again.')
        } finally {
            setLoading(false);
        }
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

    const cancel = () => {
        if (isNew) {
            document.getElementById(formId).remove();
        } else {
            setData(initialData);
            setEditing(false);
        }
    }

    return (
        <form id={formId} onSubmit={handleSubmit} className='form'>
            {loading ? (
                <Loading />
            ) : editing || isNew ? (
                <>
                    <div className='flex-grow-1 d-flex flex-wrap justify-content-center gap-2'>
                        {Array.isArray(fields) && fields.length > 0 ? (
                            fields.map((field, index) => {
                                if (field.elementType === 'input'){
                                    return (
                                        <div className="mx-auto" key={index}>
                                            <Input key={index} id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} accept={field.accept} multiple={field.multiple} error={errors[field.name]} />
                                        </div>
                                    )
                                } else {
                                    return (
                                        <div className="mx-auto" key={index}>
                                            <Select key={index} id={field.name} label={field.label || field.name} value={data[field.name] || ''} data={field.data || []} setData={setData} required={field.required || false} error={errors[field.name]} />
                                        </div>
                                    )
                                }
                            })
                        ) : <></>}
                    </div>
                    <div className="d-flex justify-content-center gap-2 mt-3 w-100">
                        <button className='btn btn-success mx-2' disabled={loading}>Save</button>
                        <button className='btn btn-danger mx-2' onClick={cancel}>Cancel</button>
                    </div>
                </>
            ) : (
                <>
                    <div className='flex-grow-1 d-flex flex-wrap gap-2'>
                        {Array.isArray(fields) && fields.length > 0 ? (
                            fields.map((field, index) => {
                                if (field.elementType === 'input'){
                                    return <Input key={index} id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} accept={field.accept} multiple={field.multiple} error={errors[field.name]} disabled={true} />
                                } else {
                                    return <Select key={index} id={field.name} label={field.label || field.name} value={data[field.name] || ''} data={field.data || []} setData={setData} required={field.required || false} error={errors[field.name]} disabled={true} />
                                }
                            })
                        ) : <></>}
                    </div>
                    <div className="d-flex justify-content-end gap-2 mt-3 w-100">
                        <button className='btn btn-primary' onClick={() => setEditing(true)}>Edit</button>
                        <button className='btn btn-danger' onClick={handleDelete}>Remove</button>
                    </div>
                </>
            )}
        </form>
    )
}

SubForm.propTypes = {
    route: PropTypes.string.isRequired,
    initialData: PropTypes.any,
    onSuccess: PropTypes.func.isRequired,
    isNew: PropTypes.bool.isRequired,
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
    ),
};

export default SubForm;
