import { Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

export default function ServiceForm({ fields, formData, errors, handleChange }) {
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
                        as={field.name === 'description' ? 'textarea' : 'input'}
                        rows={field.name === 'description' ? 3 : undefined}
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

ServiceForm.propTypes = {
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        required: PropTypes.bool,
        maxLength: PropTypes.number,
        minLength: PropTypes.number
    })).isRequired,
    formData: PropTypes.object.isRequired,
    errors: PropTypes.object,
    handleChange: PropTypes.func.isRequired
};
