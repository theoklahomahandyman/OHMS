import { Form, Button, Row, Col, Spinner, Modal, Alert, InputGroup } from 'react-bootstrap';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { profileAPI } from '../../api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';

export default function PasswordModal({ show, onHide }) {
    const profile = useSelector(state => state.profile);

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        password: '',
        confirm_password: ''
    });
    const [errors, setErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [passwordValidations, setPasswordValidations] = useState({
        hasMinLength: false,
        hasNumber: false,
        hasUpper: false,
        hasLower: false,
        hasSpecialChar: false,
        passwordsMatch: false,
        isNotSimilar: false
    });

    const fields = [
        { name: 'password', label: 'New Password' },
        { name: 'confirm_password', label: 'Confirm New Password' },
    ];

    const PASSWORD_MIN_LENGTH = 8;

    useEffect(() => {
        if (show) {
            const validatePassword = () => {
                const numberRegex = /\d/;
                const upperRegex = /[A-Z]/;
                const lowerRegex = /[a-z]/;
                const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]+/;

                const password = formData.password;
                const confirmPassword = formData.confirm_password;

                let isSimilar = false;
                if (profile) {
                    const firstNameLower = profile.first_name?.toLowerCase() || '';
                    const lastNameLower = profile.last_name?.toLowerCase() || '';
                    const emailLower = profile.email?.toLowerCase() || '';
                    const phoneLower = profile.phone?.toLowerCase() || '';

                    isSimilar = password.toLowerCase().includes(firstNameLower) ||
                                password.toLowerCase().includes(lastNameLower) ||
                                password.toLowerCase().includes(emailLower) ||
                                password.toLowerCase().includes(phoneLower);
                }

                setPasswordValidations({
                    hasMinLength: password.length >= PASSWORD_MIN_LENGTH,
                    hasNumber: numberRegex.test(password),
                    hasUpper: upperRegex.test(password),
                    hasLower: lowerRegex.test(password),
                    hasSpecialChar: specialCharRegex.test(password),
                    passwordsMatch: (password === confirmPassword) && (password !== '') && (confirmPassword !== ''),
                    isNotSimilar: !isSimilar
                });
            };
            validatePassword();
        }
    }, [formData, profile, PASSWORD_MIN_LENGTH, show]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        if (!formData.password || !formData.confirm_password) {
            toast.warning('Please fill in both password and confirm password fields!');
            setLoading(false);
            return;
        }
        try {
            await profileAPI.changePassword(formData);
            toast.success('Password successfully changed!')
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
            toast.error((error.response?.data?.password && Array.isArray(error.response?.data?.password)) ?
                error.response?.data?.password[0] :
                error.response?.data?.password ||
                'Failed to change password!');
        } finally {
            setLoading(false);
        }
    };

    const togglePasswordVisibility = () => setShowPassword(!showPassword);
    const toggleConfirmPasswordVisibility = () => setShowConfirmPassword(!showConfirmPassword);

    return (
        <Modal show={show} onHide={onHide} size='lg' centered>
            <Modal.Header closeButton>
                <Modal.Title>Change Password</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {loading ? (
                    <div className='text-center p-4'>
                        <Spinner animation='border' /><br />
                        <p className='mt-2'>Loading...</p>
                    </div>
                ) : (
                    <Form className='mx-5'>
                        {/* Change Password Form */}
                        <Row className='justify-content-center'>
                            {fields.map((field) => (
                                <Col md={6} key={field.name} className='mb-4'>
                                    <Form.Group>
                                        <Form.Label className='d-block'>{field.label}</Form.Label>
                                        <InputGroup className='mx-auto' style={{ maxWidth: '350px' }}>
                                            <Form.Control
                                                required
                                                type={field.name === 'password' ?
                                                    (showPassword ? 'text' : 'password') :
                                                    (showConfirmPassword ? 'text' : 'password')}
                                                value={formData[field.name] || ''}
                                                onChange={(e) => setFormData({
                                                    ...formData,
                                                    [field.name]: e.target.value
                                                })}
                                                isInvalid={!!errors[field.name] ||
                                                    (field.name === 'confirm_password' &&
                                                    !passwordValidations.passwordsMatch &&
                                                    formData.confirm_password)}
                                                minLength={PASSWORD_MIN_LENGTH}
                                                className='mx-auto rounded'
                                                style={{ maxWidth: '350px' }}
                                            />
                                            <InputGroup.Text style={{ cursor: 'pointer' }} onClick={field.name === 'password' ? togglePasswordVisibility : toggleConfirmPasswordVisibility}>
                                                {field.name === 'password' ?
                                                    (showPassword ? <FaEyeSlash /> : <FaEye />) :
                                                    (showConfirmPassword ? <FaEyeSlash /> : <FaEye />)}
                                            </InputGroup.Text>
                                        </InputGroup>
                                        <Form.Control.Feedback type='invalid'>
                                            {(errors[field.name] && Array.isArray(errors[field.name])) ?
                                                errors[field.name].join(' ') :
                                                errors[field.name] ||
                                                (field.name === 'confirm_password' && !passwordValidations.passwordsMatch && 'Passwords do not match')}
                                        </Form.Control.Feedback>
                                    </Form.Group>
                                </Col>
                            ))}
                        </Row>
                        {/* Password Requirements */}
                        <Row className='justify-content-center'>
                            <Col md={10}>
                                <Alert variant='info' className='p-2'>
                                    <p className='mb-1 text-center'><strong>Password Requirements:</strong></p>
                                    <ul className='mb-0 text-center list-unstyled'>
                                        <li className={passwordValidations.hasMinLength ? 'text-success' : ''}>
                                            Minimum {PASSWORD_MIN_LENGTH} characters
                                        </li>
                                        <li className={passwordValidations.hasNumber ? 'text-success' : ''}>
                                            At least one number
                                        </li>
                                        <li className={passwordValidations.hasUpper ? 'text-success' : ''}>
                                            At least one uppercase letter
                                        </li>
                                        <li className={passwordValidations.hasLower ? 'text-success' : ''}>
                                            At least one lowercase letter
                                        </li>
                                        <li className={passwordValidations.hasSpecialChar ? 'text-success' : ''}>
                                            At least one special character
                                        </li>
                                        <li className={passwordValidations.isNotSimilar ? 'text-success' : ''}>
                                            Not similar to personal information
                                        </li>
                                    </ul>
                                </Alert>
                            </Col>
                        </Row>
                        {/* Password Match Indicator */}
                        {formData.confirm_password && !passwordValidations.passwordsMatch && (
                            <Row className='justify-content-center mb-3'>
                                <Col md={10}>
                                    <Alert variant='danger' className='p-2 text-center'>
                                        Passwords do not match!
                                    </Alert>
                                </Col>
                            </Row>
                        )}
                        {/* Overall Error Indicator */}
                        {Object.keys(errors).length > 0 && (
                            <Alert variant='danger' className='text-center'>
                                Please fix form errors
                            </Alert>
                        )}
                    </Form>
                )}
            </Modal.Body>
            <Modal.Footer className='justify-content-center'>
                <div className='text-center m-2'>
                    <Button variant='secondary' className='me-2 mx-5' onClick={onHide}>
                        Cancel
                    </Button>
                    <Button variant='primary'
                        type='button'
                        onClick={handleSubmit}
                        disabled={loading ||
                            !passwordValidations.passwordsMatch ||
                            !Object.values(passwordValidations).every(Boolean)}
                    >
                        {loading ? (
                            <Spinner as='span' animation='border' size='sm' className='me-2' />
                        ) : 'Change Password'}
                    </Button>
                </div>
            </Modal.Footer>
        </Modal>
    );
};

PasswordModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired
};
