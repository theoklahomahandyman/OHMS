import PropTypes from 'prop-types';
import { useState } from 'react';
import Loading from './Loading';
import api from '../../api';

function Form ({ children, method, route, data, title, onSuccess, onError, setErrors }) {
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        console.log(data)
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
            <h1 className='modal-title text-center'>{title}</h1>
            {loading ? <Loading /> :
                <div className='modal-body'>
                    {children}
                </div>
            }
            <button className='btn btn-primary mb-3 mx-auto d-block' disabled={loading}>{title}</button>
        </form>
    )
}

Form.propTypes = {
    children: PropTypes.node.isRequired,
    method: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    data: PropTypes.any,
    title: PropTypes.string.isRequired,
    onSuccess: PropTypes.func.isRequired,
    onError: PropTypes.func.isRequired,
    setErrors: PropTypes.func,
};

export default Form;
