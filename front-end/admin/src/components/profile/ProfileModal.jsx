import { Form, Button, Row, Col, Spinner, Modal, Alert } from 'react-bootstrap';
import { updateProfile } from '../../store/profileSlice';
import { useDispatch, useSelector } from 'react-redux';
import { useState, useEffect, useMemo } from 'react';
import { profileAPI } from '../../api';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';

export default function ProfileModal({ show, onHide }) {
    const dispatch = useDispatch();
    const profile = useSelector(state => state.profile)

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: ''
    });
    const [initialData, setInitialData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: ''
    });
    const [errors, setErrors] = useState({});
    const [profileValidations, setProfileValidations] = useState({
        first_name: {
            hasMinLength: false,
            hasMaxLength: false,
            hasNoSpecialChar: false,
            hasNoNumber: false,
        },
        last_name: {
            hasMinLength: false,
            hasMaxLength: false,
            hasNoSpecialChar: false,
            hasNoNumber: false,
        },
        email: {
            hasMinLength: false,
            hasMaxLength: false,
            hasFormat: false,
            hasNoSpecialChar: false,
        },
        phone: {
            hasMinLength: false,
            hasMaxLength: false,
            hasFormat: false,
            hasOnlyDigits: false,
        }
    });

    const fields = useMemo(() => [
        { name: 'first_name', label: 'First Name', type: 'text', max: 100, min: 2 },
        { name: 'last_name', label: 'Last Name', type: 'text', max: 100, min: 2 },
        { name: 'email', label: 'Email Address', type: 'email', maxLength: 255, min: 8 },
        { name: 'phone', label: 'Phone Number', type: 'text', max: 17, min: 16 },
    ], []);

    useEffect(() => {
        if (profile) {
            setFormData({
                first_name: profile.first_name || '',
                last_name: profile.last_name || '',
                email: profile.email || '',
                phone: profile.phone || ''
            });
            setInitialData({
                first_name: profile.first_name || '',
                last_name: profile.last_name || '',
                email: profile.email || '',
                phone: profile.phone || ''
            });
        }
    }, [profile]);

    useEffect(() => {
        if (show) {
            const validateProfile = () => {
                const firstName = formData.first_name;
                const lastName = formData.last_name;
                const email = formData.email;
                const phone = formData.phone;
                const rawPhone = phone.replace(/\D/g, '')

                setProfileValidations({
                    first_name: {
                        hasMinLength: firstName.length >= fields[0].min,
                        hasMaxLength: firstName.length <= fields[0].max,
                        hasNoSpecialChar: !/[^a-zA-Z]/.test(firstName),
                        hasNoNumber: !/\d/.test(firstName),
                    },
                    last_name: {
                        hasMinLength: lastName.length >= fields[1].min,
                        hasMaxLength: lastName.length <= fields[1].max,
                        hasNoSpecialChar: !/[^a-zA-Z]/.test(lastName),
                        hasNoNumber: !/\d/.test(lastName),
                    },
                    email: {
                        hasMinLength: email.length >= fields[2].min,
                        hasMaxLength: email.length <= fields[2].max,
                        hasFormat: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),
                        hasNoSpecialChar: !/[^a-zA-Z0-9@._-]/.test(email),
                    },
                    phone: {
                        hasMinLength: phone.length >= fields[3].min,
                        hasMaxLength: phone.length <= fields[3].max,
                        hasFormat: formData.phone === formatPhone(rawPhone),
                        hasOnlyDigits: /^\+$/.test(phone),
                    }
                });
            }
            validateProfile();
        }
    }, [formData, fields, profile, show]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        if (!formData.first_name || !formData.last_name || !formData.email || !formData.phone) {
            toast.warning('Plese fill in all profile fields!');
            setLoading(false);
            return;
        }
        try {
            await profileAPI.updateProfile(formData);
            dispatch(updateProfile(formData));
            toast.success('Profile successfully updated!');
            onHide();
        } catch (error) {
            setErrors(error.response?.data || {});
            toast.error('Failed to update profile!');
        } finally {
            setLoading(false);
        }
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

    const isFormUnchanged = useMemo(() => {
        if (!initialData) return true;
        const currentPhone = formData.phone.replace(/\D/g, '');
        const initialPhone = initialData.phone.replace(/\D/g, '') || '';
        return (
            formData.first_name === initialData.first_name &&
            formData.last_name === initialData.last_name &&
            formData.email === initialData.email &&
            currentPhone === initialPhone
        );
    }, [formData, initialData]);

    return (
        <Modal show={show} onHide={onHide} size='lg' centered>
            <Modal.Header closeButton>
                <Modal.Title>Update Profile</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {loading ? (
                    <div className='text-center p-4'>
                        <Spinner animation='border' /><br />
                        <p className='mt-2'>Loading...</p>
                    </div>
                ) : (
                    <Form className='mx-5'>
                        <Row className='justify-content-center'>
                            {fields.map((field) => (
                                <Row key={field.name}>
                                    <Col md={6} className='mb-3'>
                                        <Form.Group>
                                            <Form.Label className='d-block'>{field.label}</Form.Label>
                                            <Form.Control required
                                                type={field.type}
                                                name={field.name}
                                                value={formData[field.name] || ''}
                                                onChange={(e) => handleChange(e)}
                                                isInvalid={!!errors[field.name]}
                                                maxLength={field.max}
                                                minLength={field.min}
                                                className='mx-auto'
                                                style={{ maxWidth: '350px' }}
                                            />
                                            <Form.Control.Feedback type='invalid'>
                                                {errors[field.name]?.join(' ')}
                                            </Form.Control.Feedback>
                                        </Form.Group>
                                    </Col>
                                    <Col md={6}>
                                        <Alert variant='info' className='p-2'>
                                            <p className='mb-1 text-center'><strong>{field.label} Requirements:</strong></p>
                                            <ul className='mb-0 text-center list-unstyled'>
                                                <li className={profileValidations[field.name].hasMinLength ? 'text-success' : ''}>
                                                    Minimum {field.min} characters
                                                </li>
                                                <li className={profileValidations[field.name].hasMinLength ? 'text-success' : ''}>
                                                    Maximum {field.max} characters
                                                </li>
                                            </ul>
                                        </Alert>
                                    </Col>
                                </Row>
                            ))}
                        </Row>
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
                        onClick={(e) => handleSubmit(e)}
                        disabled={loading || !Object.values(profileValidations).every(Boolean) || isFormUnchanged}
                    >
                        {loading ? (
                            <Spinner as='span' animation='border' size='sm' className='me-2' />
                        ) : 'Save Changes'}
                    </Button>
                </div>
            </Modal.Footer>
        </Modal>
    );
};

ProfileModal.propTypes = {
    show: PropTypes.bool.isRequired,
    onHide: PropTypes.func.isRequired
};
