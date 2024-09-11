import { handleChange } from '../../utils/change';
import PropTypes from 'prop-types';

function Select ({ id, label, required, value, data, setData, error, disabled, customChange }) {
    const onChange = (event) => {
        handleChange(event, setData);
    }

    return (
        <div className='form-group text-center'>
            <label htmlFor={label}>{label}</label>
            <div className='input-group'>
                <select name={id} id={id} className='form-control' value={value} required={required} onChange={customChange ? customChange : onChange} disabled={disabled === true ? disabled : false}>
                    <option value=''>Select {label}</option>
                    {data.map((option, index) => (
                        <option key={index} value={option.value}>{option.label}</option>
                    ))}
                </select>
            </div>
            {error && <div className='alert alert-danger mt-2'>{error}</div>}
        </div>
    )
}

Select.propTypes = {
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    required: PropTypes.bool.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.object, PropTypes.number]).isRequired,
    data: PropTypes.arrayOf(
        PropTypes.shape({
            value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
            label: PropTypes.string.isRequired
        })
    ).isRequired,
    setData: PropTypes.func.isRequired,
    error: PropTypes.string,
    disabled: PropTypes.bool,
    customChange: PropTypes.func,
};

export default Select;
