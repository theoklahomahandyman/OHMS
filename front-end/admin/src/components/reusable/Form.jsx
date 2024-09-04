import PropTypes from 'prop-types';
import { useState } from 'react';
import Loading from './Loading';
import Select from './Select';
import Input from './Input';
import api from '../../api';

function Form ({ fields, method, route, data, setData, buttonText, buttonStyle, onSuccess, onError, errors, setErrors, children }) {
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            if (method === 'post'){
                const response = await api.post(route, data);
                onSuccess(response.data)
            } else if (method === 'patch') {
                const response = await api.patch(route, data);
                onSuccess(response.data)
            } else if (method === 'put') {
                const response = await api.put(route, data);
                onSuccess(response.data)
            } else if (method === 'delete') {
                const response = await api.delete(route);
                onSuccess(response)
            }
        } catch (error) {
            if (error.response && error.response.data) {
                if (setErrors) {
                    onError(error.response.data, setErrors);
                } else {
                    onError(error.response.data)
                }
            } else {
                onError({ non_field_errors: ['An unexpected error occured.']}, setErrors);
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit = {handleSubmit} className='form'>
            {loading ? <Loading /> :
                <div className='modal-body'>
                    {Array.isArray(fields) && fields.length > 0 ? (
                        fields.map((field, index) => {
                            if (field.elementType === 'input'){
                                return <Input key={index} id={field.name} label={field.label || field.name} type={field.type || 'text'} value={data[field.name] || ''} setData={setData} required={field.required || false} maxLength={field.maxLength} minLength={field.minLength} accept={field.accept} multiple={field.multiple} error={errors[field.name]} />
                            } else {
                                return <Select key={index} id={field.name} label={field.label || field.name} value={data[field.name] || ''} data={field.data || []} setData={setData} required={field.required || false} error={errors[field.name]} />
                            }
                        })

                    ) : <></>}
                    {children}
                </div>
            }
            <button className={`btn btn-${buttonStyle} mb-3 mx-auto d-block`} disabled={loading}>{buttonText}</button>
        </form>
    )
}

Form.propTypes = {
    children: PropTypes.node,
    method: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    data: PropTypes.any,
    setData: PropTypes.func,
    errors: PropTypes.any,
    buttonText: PropTypes.string.isRequired,
    buttonStyle: PropTypes.string.isRequired,
    onSuccess: PropTypes.func.isRequired,
    onError: PropTypes.func.isRequired,
    setErrors: PropTypes.func,
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

export default Form;
