import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { makeRequest } from '../../../api';
import Select from '../input/Select';
import Input from '../input/Input';
import PropTypes from 'prop-types';
import Loading from '../Loading';

function SubForm ({ fields, route, initialData, fetchData, fetchRelatedData, isNew, id, name }) {
    const [data, setData] = useState(initialData || {});
    const [files, setFiles] = useState({});
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [editing, setEditing] = useState(false);

    const formId = `subform-${Math.random().toString(36).substr(2, 9)}`;

    useEffect(() => {
        if (!isNew) {
            setEditing(false);
        }
    }, [isNew]);

    const triggerEditing = () => {
        setEditing(true);
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData();
        for (const key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                formData.append(key, data[key]);
            }
        }
        for (const key in files) {
            if (Object.prototype.hasOwnProperty.call(files, key)) {
                formData.append(key, files[key]);
            }
        }

        try {
            if (isNew){
                await makeRequest('post', route, formData);
                toast.success(`${name} Successfully Added!`);
                setEditing(false);
                setData({});
                if (fetchRelatedData) {
                    fetchRelatedData();
                }
                fetchData();
            } else if (editing) {
                await makeRequest('patch', `${route}${id}/`, formData);
                toast.success(`${name} Successfully Edited!`);
                setEditing(false);
                if (fetchRelatedData) {
                    fetchRelatedData();
                }
                fetchData();
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
            await makeRequest('delete', `${route}${id}/`);
            toast.success(`${name} Successfully Removed!`);
            fetchRelatedData();
            fetchData();
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
        <>
            <form id={formId} onSubmit={handleSubmit} className='form' encType='multipart/form-data'>
                {loading ? (
                    <Loading />
                ) : (
                    <>
                        <div className='flex-grow-1 d-flex flex-wrap justify-content-center gap-2'>
                            {Array.isArray(fields) && fields.length > 0 ? (
                                fields.map((field, index) => {
                                    if (field.elementType === 'input'){
                                        if (field.type === 'file') {
                                            return (
                                                <div className='mx-auto' key={index}>
                                                    <Input id={field.name} label={field.label || field.name} type={field.type} value={files[field.name] || ''} setFiles={setFiles} required={field.required || false} accept={field.accept} multiple={field.multiple} error={errors[field.name]} disabled={field.disabled || !editing && !isNew} />
                                                    {data[field.name] && (
                                                        <div className="file-info">
                                                            <a href={`http://localhost:8000${data[field.name]}`} target="_blank" rel="noopener noreferrer">{data[field.name].split('/').pop()}</a>
                                                        </div>
                                                    )}
                                                </div>
                                            )
                                        } else {
                                            return (
                                                <div className="mx-auto" key={index}>
                                                    <Input id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} maxValue={field.maxValue} minValue={field.minValue} accept={field.accept} multiple={field.multiple} error={errors[field.name]} disabled={field.disabled || !editing && !isNew} />
                                                </div>
                                            )
                                        }
                                    } else {
                                        return (
                                            <div className="mx-auto" key={index}>
                                                <Select id={field.name} label={field.label || field.name} value={data[field.name] || ''} data={field.data || []} setData={setData} required={field.required || false} error={errors[field.name]} customChange={field.customChange} disabled={field.disabled || !editing && !isNew} />
                                            </div>
                                        )
                                    }
                                })
                            ) : <></>}
                        </div>
                        {isNew || editing ? (
                            <div className='d-flex justify-content-center gap-2 mt-3 w-100 mb-3'>
                                <button className='btn btn-success mx-2' disabled={loading} type='submit'>Save</button>
                                <button className='btn btn-danger mx-2' onClick={cancel} type='button'>Cancel</button>
                            </div>
                        ) : (<></>)}
                    </>
                )}
            </form>
            {!isNew && !editing ? (
                <div className='d-flex justify-content-center gap-2 mt-3 w-100 mb-3'>
                    {/* edit button submitting rather than going into edit state */}
                    <button className='btn btn-primary mx-2' onClick={(triggerEditing)} type='button'>Edit</button>
                    <button className='btn btn-danger mx-2' onClick={handleDelete} type='button'>Remove</button>
                </div>
            ) : (<></>)}
        </>
    )
}

SubForm.propTypes = {
    route: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    fetchData: PropTypes.func.isRequired,
    fetchRelatedData: PropTypes.func,
    isNew: PropTypes.bool.isRequired,
    fields: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            type: PropTypes.string,
            required: PropTypes.bool.isRequired,
            elementType: PropTypes.string.isRequired,
            maxLength: PropTypes.number,
            minLength: PropTypes.number,
            data: PropTypes.arrayOf(PropTypes.shape({
                value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
                label: PropTypes.string.isRequired
            })),
            customChange: PropTypes.func,
            disabled: PropTypes.bool,
        })
    ).isRequired,

    id: PropTypes.number,
    initialData: PropTypes.any,
};

export default SubForm;
