import { handleChange, handleFileChange } from '../../utils/change';
import PropTypes from 'prop-types';
import { useState } from 'react';

function Input ({ id, label, type, value, required, setData, setFiles, placeholder, maxLength, minLength, error, disabled }) {
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

    const onChange = (event) => {
        if (type === 'file') {
            handleFileChange(event, setFiles);
        } else {
            handleChange(event, setData);
        }
    }

    return (
        <div className='form-group text-center'>
            <label htmlFor={label}>{label}</label>
            <div className='input-group '>
                <input className={`${type === 'file' ? 'form-control-file' : 'form-control'}`} id={id} name={id} type={showPassword ? 'text' : type} value={type === 'file' ? undefined : value} onChange={onChange} required={required} placeholder={placeholder} maxLength={maxLength} minLength={minLength} accept={type === 'file' ? 'image/*': undefined} multiple={type === 'file' ? true : undefined} disabled={disabled === true ? disabled : false} autoComplete={autoCompleteType} checked={type === 'checkbox' ? !!value: undefined} step={type === 'number' ? '0.01' : undefined} />
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
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.object, PropTypes.number, PropTypes.bool, PropTypes.array]).isRequired,
    setData: PropTypes.func,
    setFiles: PropTypes.func,
    placeholder: PropTypes.string,
    maxLength: PropTypes.number,
    minLength: PropTypes.number,
    error: PropTypes.string,
    disabled: PropTypes.bool,
};

export default Input;
