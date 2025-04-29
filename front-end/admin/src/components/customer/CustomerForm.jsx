import { Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

export default function CustomerForm({ fields, formData, setFormData, errors }) {
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
        const { name, value } = event.target;
        if (name === 'phone') {
            const digits = value.replace(/\D/g, '');
            const formattedPhoneNumber = formatPhone(digits)
            setFormData((prevData) => ({
                ...prevData,
                phone: formattedPhoneNumber
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
                    <Form.Label>{ field.label }</Form.Label>
                    <Form.Control
                        type={field.type}
                        name={field.name}
                        value={formData[field.name] || ''}
                        onChange={handleChange}
                        required={field.required}
                        isInvalid={!!errors[field.name]}
                        as={field.name === 'notes' ? 'textarea' : 'input'}
                        rows={field.name === 'notes' ? 3 : undefined}
                        maxLength={field.maxLength}
                        minLength={field.minLength}
                    />
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

CustomerForm.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool,
        maxLength: PropTypes.number,
        minLength: PropTypes.number
    })).isRequired,
    formData: PropTypes.object.isRequired,
    setFormData: PropTypes.func.isRequired,
    errors: PropTypes.object,
};
