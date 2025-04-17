import { Form, Button, Row, Col, Spinner, Modal, Alert } from 'react-bootstrap';
import { updateProfile } from '../../store/profileSlice';
import { useDispatch, useSelector } from 'react-redux';
import { useState, useEffect } from 'react';
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
    const [errors, setErrors] = useState({});

    const fields = [
        { name: 'first_name', label: 'First Name', type: 'text', required: true, maxLength: 100, minLength: 2 },
        { name: 'last_name', label: 'Last Name', type: 'text', required: true, maxLength: 100, minLength: 2 },
        { name: 'email', label: 'Email', type: 'text', required: true, maxLength: 255, minLength: 8 },
        { name: 'phone', label: 'Phone Number', type: 'text', required: true, maxLength: 17, minLength: 16 },
    ];

    useEffect(() => {
        if (profile) {
            setFormData({
                first_name: profile.first_name || '',
                last_name: profile.last_name || '',
                email: profile.email || '',
                phone: profile.phone || ''
            });
        }
    }, [profile]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
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
                                <Col md={6} key={field.name} className='mb-3'>
                                    <Form.Group>
                                        <Form.Label className='d-block'>{field.label}</Form.Label>
                                        <Form.Control
                                            type={field.type}
                                            value={formData[field.name] || ''}
                                            onChange={(e) => setFormData({
                                                ...formData,
                                                [field.name]: e.target.value
                                            })}
                                            required={field.required}
                                            isInvalid={!!errors[field.name]}
                                            maxLength={field.maxLength}
                                            minLength={field.minLength}
                                            className='mx-auto'
                                            style={{ maxWidth: '350px' }}
                                        />
                                        <Form.Control.Feedback type='invalid'>
                                            {errors[field.name]?.join(' ')}
                                        </Form.Control.Feedback>
                                    </Form.Group>
                                </Col>
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
                    <Button variant='primary' type='button' onClick={(e) => handleSubmit(e)} disabled={loading}>
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
