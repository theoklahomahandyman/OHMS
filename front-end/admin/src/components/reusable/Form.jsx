import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import { useState } from 'react';
import FormSet from './FormSet';
import Loading from './Loading';
import Select from './Select';
import Input from './Input';
import api from '../../api';

function Form ({ fields, formsets, method, route, baseRoute, id, initialData, buttonText, buttonStyle, onSuccess, children, customError }) {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(initialData || {});
    const [files, setFiles] = useState({});
    const [errors, setErrors] = useState({});

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData();
        for (const key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                formData.append(key, data[key]);
            }
        }
        if (files.uploaded_images) {
            const uploadedImages = Array.isArray(files.uploaded_images) ? files.uploaded_images : [files.uploaded_images];
            uploadedImages.forEach((file) => {
                formData.append('uploaded_images', file);
            });
        }
        try {
            if (method === 'post'){
                console.log(files)
                const response = await api.post(route, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
                onSuccess(response.data)
            } else if (method === 'patch') {
                const response = await api.patch(route, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
                onSuccess(response.data)
            } else if (method === 'put') {
                const response = await api.put(route, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
                onSuccess(response.data)
            } else if (method === 'delete') {
                const response = await api.delete(route);
                onSuccess(response)
            }
        } catch (error) {
            console.log(error.response.data)
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

    const handleError = (data) => {
        if (method === 'delete') {
            toast.error('An error occurred so nothing was deleted. Please try again.');
        } else {
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
            if (customError !== undefined) {
                toast.error(customError);
            }
        }
    }

    const removeImage = async (id) => {
        try {
            api.delete(`${baseRoute}image/${id}/`);
            window.location.reload();
            toast.success('Image successfully removed!');
        } catch (error) {
            toast.error(error);
        }
    }

    return (
        <>
            <form onSubmit={handleSubmit} className="form" encType='multipart/form-data'>
                {loading ? <Loading /> : (
                    <div className="row">
                        {Array.isArray(fields) && fields.length > 0 ? (
                            fields.map((field, index) => (
                                <div key={index} className="col-6 mx-auto mb-3">
                                    {field.elementType === 'input' ? (
                                        field.type === 'file' ? (
                                            <>
                                                <Input id={field.name} label={field.label || field.name} type={field.type} value={files[field.name] || ''} setFiles={setFiles} required={field.required || false} accept={field.accept} multiple={field.multiple} error={errors[field.name]} />
                                                {(field.name === 'uploaded_images') && (data.images) && (data.images.length > 0) && (
                                                    <div className="file-info">
                                                        {data.images.map((image, index) => (
                                                            <div key={index} className='mb-3'>
                                                                <a href={`http://localhost:8000${image.image}`} target="_blank" rel="noopener noreferrer">{image.image.split('/').pop()}</a>
                                                                <button className="btn btn-sm btn-danger ml-2" type='button' onClick={() => removeImage(image.id)}>Remove</button>
                                                            </div>
                                                        ))}
                                                    </div>
                                                )}
                                            </>
                                        ) : (
                                            <Input key={index} id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} maxValue={field.maxValue} minValue={field.minValue} accept={field.accept} multiple={field.multiple} error={errors[field.name]} disabled={field.disabled} />
                                        )
                                    ) : (
                                        <Select key={index} id={field.name} label={field.label || field.name} value={data[field.name] || ''} data={field.data || []} setData={setData} required={field.required || false} error={errors[field.name]} customChange={field.customChange} />
                                    )}
                                </div>
                            ))
                        ) : null}
                        {children}
                    </div>
                )}
                <button className={`btn btn-lg btn-${buttonStyle} mb-3 mx-auto d-block`} disabled={loading} type="submit">
                    {buttonText}
                </button>
            </form>
            {Array.isArray(formsets) && formsets.length > 0 ? formsets.map((formset, index) => (
                <FormSet key={`${index}-${formset.entity}-formset`} entity={formset.entity} fields={formset.fields} route={formset.route} id={id} />
            )) : null}
        </>
    );
}

Form.propTypes = {
    method: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    buttonText: PropTypes.string.isRequired,
    buttonStyle: PropTypes.string.isRequired,
    onSuccess: PropTypes.func.isRequired,

    id: PropTypes.any,
    children: PropTypes.node,
    initialData: PropTypes.any,
    customError: PropTypes.string,
    baseRoute: PropTypes.string,
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
            disabled: PropTypes.bool,
        })
    ),
    formsets: PropTypes.arrayOf(
        PropTypes.shape({
            entity: PropTypes.string.isRequired,
            route: PropTypes.string.isRequired,
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
                })
            ).isRequired,
        })
    ),
};

export default Form;
