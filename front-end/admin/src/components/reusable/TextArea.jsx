import { handleChange } from '../../utils/change';
import PropTypes from 'prop-types';

function TextArea ({ id, label, value, required, setData, placeholder, maxLength, minLength, error, disabled }) {

    const onChange = (event) => {
        handleChange(event, setData);
    }

    return (
        <div className='form-group text-center'>
            <label htmlFor={label}>{label}</label>
            <div className='input-group '>
                <textarea className='form-control' id={id} name={id} value={value} onChange={onChange} required={required} placeholder={placeholder} maxLength={maxLength} minLength={minLength} disabled={disabled === true ? disabled : false} rows='3' cols='165'></textarea>
            </div>
            {error && <div className='alert alert-danger mt-2'>{error}</div>}
        </div>
    )
}

TextArea.propTypes = {
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    required: PropTypes.bool.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.object, PropTypes.number, PropTypes.bool, PropTypes.array]),
    setData: PropTypes.func,
    placeholder: PropTypes.string,
    maxLength: PropTypes.number,
    minLength: PropTypes.number,
    error: PropTypes.string,
    disabled: PropTypes.bool,
};

export default TextArea;
