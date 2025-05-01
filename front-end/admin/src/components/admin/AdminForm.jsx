import { Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

export default function AdminForm({ fields, formData, setFormData, errors }) {
    const formatPhone = (digits) => {
        // Remove any non-digit characters to simplify the formatting logic
        const cleanDigits = digits.replace(/\D/g, '');
        // Start building the formatted number incrementally
        let formatted = '';
        if (cleanDigits.length > 0) {
            // First digit
            formatted += cleanDigits[0];
        }
        if (cleanDigits.length > 1) {
            // Next three digits inside parentheses
            formatted += ' (' + cleanDigits.slice(1, 4);
        }
        if (cleanDigits.length >= 4) {
            // Close the parentheses
            formatted += ') ';
        }
        if (cleanDigits.length >= 5) {
            // Next three digits after the parentheses
            formatted += cleanDigits.slice(4, 7);
        }
        if (cleanDigits.length >= 7) {
            // Add a dash after the next three digits
            formatted += '-' + cleanDigits.slice(7, 11);
        }
        return formatted;
    };

    const handleChange = (event) => {
        const { name, value, type, checked } = event.target;
        if (name === 'phone') {
            const digits = value.replace(/\D/g, '');
            const formattedPhoneNumber = formatPhone(digits)
            setFormData((prevData) => ({
                ...prevData,
                phone: formattedPhoneNumber
            }));
        } else if (type === 'checkbox') {
            setFormData((prevData) => ({
                ...prevData,
                [name]: checked,
            }));
        } else {
            setFormData((prevData) => ({
                ...prevData,
                [name]: value,
            }));
        }
    };

    return (
        <Form>
            { fields.map((field) => (
                <Form.Group key={field.name} className='mb-3'>
                    { field.type === 'checkbox' ? (
                        <div className='d-flex justify-content-center w-100'>
                            <div className='d-flex align-items-center gap-2'>
                                <Form.Check
                                    type='checkbox'
                                    name={field.name}
                                    checked={formData[field.name] || false}
                                    onChange={handleChange}
                                    className='flex-shrink-0'
                                    style={{ marginTop: '-22px' }}
                                />
                                <span style={{ color: formData[field.name] ? 'green' : 'red', fontWeight: 500, lineHeight: '1.5rem' }}>
                                    { formData[field.name] ? 'ACTIVE' : 'INACTIVE' }
                                </span>
                            </div>
                        </div>
                    ) : (
                        <>
                            <Form.Label>{ field.label }</Form.Label>
                            <Form.Control
                                type={field.type}
                                name={field.name}
                                value={formData[field.name] || ''}
                                onChange={handleChange}
                                required={field.required}
                                isInvalid={!!errors[field.name]}
                            />
                        </>
                    )}
                    { errors[field.name] && (
                        <Form.Control.Feedback type='invalid'>
                            { errors[field.name] }
                        </Form.Control.Feedback>
                    )}
                </Form.Group>
            ))}
        </Form>
    );
};

AdminForm.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool
    })).isRequired,
    formData: PropTypes.object.isRequired,
    errors: PropTypes.object,
    setFormData: PropTypes.func.isRequired
};
