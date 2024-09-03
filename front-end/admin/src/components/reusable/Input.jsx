import { handleChange } from '../../utils/change';
import PropTypes from 'prop-types';
import { useState } from 'react';

function Input ({ id, label, type, value, required, setData, placeholder, maxLength, minLength, accept, multiple, error }) {
    const [showPassword, setShowPassword] = useState(false);

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword)
    };

    let autoCompleteType = undefined;

    if (type === 'password') {
        autoCompleteType = 'new-password';
    } else if (type === 'text' && id === 'phone') {
        autoCompleteType = 'tel';
    } else if (type === 'email') {
        autoCompleteType = 'email';
    } else if (type === 'text' && id === 'first_name') {
        autoCompleteType = 'given-name';
    } else if (type === 'text' && id === 'last_name') {
        autoCompleteType = 'family-name';
    } else {
        autoCompleteType = undefined;
    }

    return (
        <div className='form-group text-center'>
            <label htmlFor={label}>{label}</label>
            <div className='input-group'>
                <input className='form-control' id={id} name={id} type={showPassword ? 'text' : type} value={value} required={required} onChange={(event) => handleChange(event, setData)} placeholder={placeholder} maxLength={maxLength} minLength={minLength} accept={type === 'file' ? accept: undefined} multiple={type === 'file' ? multiple : undefined} autoComplete={autoCompleteType}/>
                {type === 'password' && (<button className='btn btn-outline-secondary' type='button' onClick={togglePasswordVisibility}>{showPassword ? 'Hide' : 'Show'}</button>)}
            </div>
            {error && <div className='alert alert-danger mt-2'>{error}</div>}
        </div>
    )
}

Input.propTypes = {
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    required: PropTypes.bool.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.object, PropTypes.number]).isRequired,
    setData: PropTypes.func.isRequired,
    placeholder: PropTypes.string,
    maxLength: PropTypes.number,
    minLength: PropTypes.number,
    accept: PropTypes.string,
    multiple: PropTypes.bool,
    error: PropTypes.string,
};

export default Input;
