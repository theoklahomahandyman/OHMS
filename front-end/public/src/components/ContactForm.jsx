import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import submit_contact_form from '../api';
import { toast } from 'react-toastify';
import Loading from './Loading';

function ContactForm() {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });
    const [data, setData] = useState({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });

    const [confirmEmail, setConfirmEmail] = useState('');

    useEffect(() => {
        const checkEmail = () => {
            if (data['email'] !== confirmEmail) {
                setErrors((prevData) => ({
                    ...prevData,
                    ['confirm_email']: 'Emails must match!'
                }));
            } else {
                setErrors((prevData) => {
                    const updatedErrors = { ...prevData };
                    delete updatedErrors.confirm_email;
                    return updatedErrors;
                });
            }
        }
        checkEmail();
    }, [data, confirmEmail]);

    const onSuccess = () => {
        setData({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });
        setErrors({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });
        setConfirmEmail('');
        toast.success('Your request has been successfully submitted. We will be in touch soon!');
    };

    const handleError = (data) => {
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
    };

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
            setData((prevData) => ({
                ...prevData,
                phone: formattedPhoneNumber
            }));
        } else {
            setData((prevData) => ({
                ...prevData,
                [name]: value,
            }));
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData();
        for (const key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                formData.append(key, data[key]);
            }
        }
        try {
            const response = await submit_contact_form(formData);
            onSuccess(response.data);
        } catch (error) {
            if (error.response && error.response.data) {
                handleError(error.response.data);
            } else {
                handleError({ non_field_errors: ['An unexpected error occured.']});
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="signup-section" id="contact" aria-label="Contact form for Oklahoma Handyman Service">
            <Container className="px-4 px-lg-5">
                <Row className="gx-4 gx-lg-5 justify-content-center">
                    <Col md={10} lg={8} className="mx-auto text-center">
                        <i className="far fa-paper-plane fa-2x mb-2 text-white" aria-hidden="true"></i>
                        <h2 className="text-white mb-5">Contact us to get started with your project!</h2>
                        <Form id="contactForm" onSubmit={handleSubmit}>
                            {loading ? <Loading /> : (
                                <>
                                    <Row className="mb-3">
                                        {/* First name input */}
                                        <Col md={6}>
                                            <Form.Group controlId="first_name">
                                                <Form.Control type="text" placeholder="First Name" value={data.first_name} onChange={handleChange} required />
                                                {errors.first_name && <Alert variant="danger" className="mt-2">{errors.first_name}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Last name input */}
                                        <Col md={6}>
                                            <Form.Group controlId="last_name">
                                                <Form.Control type="text" placeholder="Last Name" value={data.last_name} onChange={handleChange} required />
                                                {errors.last_name && <Alert variant="danger" className="mt-2">{errors.last_name}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Email input */}
                                        <Col md={6}>
                                            <Form.Group controlId="email">
                                                <Form.Control type="email" placeholder="Email" value={data.email} onChange={handleChange} required />
                                                {errors.email && <Alert variant="danger" className="mt-2">{errors.email}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Confirm email input */}
                                        <Col md={6}>
                                            <Form.Group controlId="confirm_email">
                                                <Form.Control type="email" placeholder="Email" value={data.confirm_email} onChange={(e) => setConfirmEmail(e.target.value)} required />
                                                {errors.confirm_email && <Alert variant="danger" className="mt-2">{errors.confirm_email}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Phone number input */}
                                        <Col md={6}>
                                            <Form.Group controlId="phone">
                                                <Form.Control type="text" placeholder="Phone Number" value={data.phone} onChange={handleChange} required />
                                                {errors.phone && <Alert variant="danger" className="mt-2">{errors.phone}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Date input */}
                                        <Col md={6}>
                                            <Form.Group controlId="date">
                                                <Form.Control type="date" placeholder="Project Date" value={data.date} onChange={handleChange} required />
                                                {errors.date && <Alert variant="danger" className="mt-2">{errors.date}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Description input */}
                                        <Col md={12}>
                                            <Form.Group controlId="description">
                                                <Form.Control as="textarea" rows={6} placeholder="Description" value={data.description} onChange={handleChange} required />
                                                {errors.description && <Alert variant="danger" className="mt-2">{errors.description}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    {/* Submit button */}
                                    <Button variant="primary" type="submit" aria-label="Submit contact form" disabled={loading}>{ loading ? 'Submitting...' : 'Submit' }</Button>
                                </>
                            )}
                        </Form>
                    </Col>
                </Row>
            </Container>
        </section>
    );
}

export default ContactForm;
