import { Container, Row, Col, Form, Button, Alert, Modal } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import submit_contact_form from '../api';
import { toast } from 'react-toastify';
import Loading from './Loading';

function ContactForm() {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });
    const [data, setData] = useState({ first_name: '', last_name: '', email: '', phone: '', date: '', description: '' });

    const [confirmEmail, setConfirmEmail] = useState('');
    const [agreeTerms, setAgreeTerms] = useState(false);
    const [agreePrivacy, setAgreePrivacy] = useState(false);
    const [showTerms, setShowTerms] = useState(false);
    const [showPrivacy, setShowPrivacy] = useState(false);

    const handleShowTerms = () => setShowTerms(true);
    const handleCloseTerms = () => setShowTerms(false);
    const handleShowPrivacy = () => setShowPrivacy(true);
    const handleClosePrivacy = () => setShowPrivacy(false);

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
        setAgreeTerms(false);
        setAgreePrivacy(false);
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
        if (!agreeTerms || !agreePrivacy) {
            setErrors(prev => ({
                ...prev,
                non_field_errors: ['Please read and accept both our terms of use and privacy policy']
            }));
            return;
        }
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
                        <h3 className="text-white mb-5">Contact us to get started with your project!</h3>
                        <Form id="contactForm" onSubmit={handleSubmit}>
                            {loading ? <Loading /> : (
                                <>
                                    <Row className="mb-3">
                                        {/* First name input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="first_name">
                                                <Form.Control type="text" placeholder="First Name" value={data.first_name} onChange={handleChange} required />
                                                {errors.first_name && <Alert variant="danger" className="mt-2">{errors.first_name}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Last name input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="last_name">
                                                <Form.Control type="text" placeholder="Last Name" value={data.last_name} onChange={handleChange} required />
                                                {errors.last_name && <Alert variant="danger" className="mt-2">{errors.last_name}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Email input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="email">
                                                <Form.Control type="email" placeholder="Email" value={data.email} onChange={handleChange} required />
                                                {errors.email && <Alert variant="danger" className="mt-2">{errors.email}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Confirm email input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="confirm_email">
                                                <Form.Control type="email" placeholder="Confirm Email" value={data.confirm_email} onChange={(e) => setConfirmEmail(e.target.value)} required />
                                                {errors.confirm_email && <Alert variant="danger" className="mt-2">{errors.confirm_email}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Phone number input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="phone">
                                                <Form.Control type="text" placeholder="Phone Number" value={data.phone} onChange={handleChange} required />
                                                {errors.phone && <Alert variant="danger" className="mt-2">{errors.phone}</Alert>}
                                            </Form.Group>
                                        </Col>
                                        {/* Date input */}
                                        <Col md={6} className="mb-2">
                                            <Form.Group controlId="date">
                                                <Form.Control type="date" placeholder="Project Date" value={data.date} onChange={handleChange} required />
                                                {errors.date && <Alert variant="danger" className="mt-2">{errors.date}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        {/* Description input */}
                                        <Col md={12} className="mb-2">
                                            <Form.Group controlId="description">
                                                <Form.Control as="textarea" rows={6} placeholder="Description" value={data.description} onChange={handleChange} required />
                                                {errors.description && <Alert variant="danger" className="mt-2">{errors.description}</Alert>}
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Row className="mb-3">
                                        <Col md={12} className="d-flex flex-column align-items-center">
                                            {/* Terms of use agreement */}
                                            <Form.Group controlId="terms" className="d-flex justify-content-center align-items-center mb-2">
                                                <Form.Check
                                                    type="checkbox"
                                                    label={
                                                        <span className="text-white">
                                                            I agree to the {" "}
                                                            <span className="text-primary cursor-pointer" style={{ textDecoration: 'underline' }} onClick={handleShowTerms}>
                                                                Terms of Use
                                                            </span>
                                                        </span>}
                                                    checked={agreeTerms}
                                                    onChange={(e) => setAgreeTerms(e.target.checked)}
                                                    isInvalid={!!errors.non_field_errors}
                                                    className="me-2"
                                                />
                                            </Form.Group>
                                            {/* Privacy policy agreement */}
                                            <Form.Group controlId="privacy" className="d-flex justify-content-center align-items-center mb-2">
                                                <Form.Check
                                                    type="checkbox"
                                                    label={
                                                        <span className="text-white">
                                                            I agree to the {" "}
                                                            <span className="text-primary cursor-pointer" style={{ textDecoration: 'underline' }} onClick={handleShowPrivacy}>
                                                                Privacy Policy
                                                            </span>
                                                        </span>
                                                    }
                                                    checked={agreePrivacy}
                                                    onChange={(e) => setAgreePrivacy(e.target.checked)}
                                                    isInvalid={!!errors.non_field_errors}
                                                    className="me-2"
                                                />
                                            </Form.Group>
                                            {/* Terms of use modal */}
                                            <Modal show={showTerms} onHide={handleCloseTerms} centered>
                                                <Modal.Header closeButton>
                                                    <Modal.Title className="text-center w-100">Terms of Use</Modal.Title>
                                                </Modal.Header>
                                                <Modal.Body>
                                                    <p>By using our services, you agree to:</p>
                                                    <ul>
                                                        <li>Provide accurate information</li>
                                                        <li>Use services legally and appropriately</li>
                                                        <li>Accept our cancellation/rescheduling policy</li>
                                                    </ul>
                                                    <p>We reserve the right to refuse service and modify these terms at any time.</p>
                                                </Modal.Body>
                                                <Modal.Footer className="justify-content-center">
                                                    <Button variant="primary" onClick={handleCloseTerms}>Close</Button>
                                                </Modal.Footer>
                                            </Modal>
                                            {/* Privacy policy modal */}
                                            <Modal show={showPrivacy} onHide={handleClosePrivacy} centered>
                                                <Modal.Header closeButton>
                                                    <Modal.Title className="text-center w-100">Privacy Policy</Modal.Title>
                                                </Modal.Header>
                                                <Modal.Body>
                                                    <p>We collect information you provide through our contact form including:</p>
                                                    <ul>
                                                        <li>Name</li>
                                                        <li>Email address</li>
                                                        <li>Phone number</li>
                                                        <li>Project details</li>
                                                    </ul>
                                                    <p>This data is used solely for processing your service request and is stored securely using:</p>
                                                    <ul>
                                                        <li>HTTPS encryption</li>
                                                        <li>Password hashing</li>
                                                        <li>JWT token authentication</li>
                                                        <li>Encrypted database storage</li>
                                                    </ul>
                                                </Modal.Body>
                                                <Modal.Footer className="justify-content-center">
                                                    <Button variant="primary" onClick={handleClosePrivacy}>Close</Button>
                                                </Modal.Footer>
                                            </Modal>
                                            {errors.non_field_errors && (
                                                <Alert variant="danger" className="mt-2">
                                                    {errors.non_field_errors}
                                                </Alert>
                                            )}
                                        </Col>
                                    </Row>
                                    {/* Submit button */}
                                    <Button variant="primary" type="submit" aria-label="Submit contact form" disabled={loading || !agreeTerms || !agreePrivacy}>{ loading ? 'Submitting...' : 'Submit' }</Button>
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
