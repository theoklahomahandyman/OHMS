import { Form, Button, Row, Col, Spinner } from 'react-bootstrap';
import { profileAPI } from '../../api';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';

export default function ProfileForm() {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const fields = [
        { name: 'first_name', label: 'First Name', type: 'text', required: true, maxLength: 100, minLength: 2 },
        { name: 'last_name', label: 'Last Name', type: 'text', required: true, maxLength: 100, minLength: 2 },
        { name: 'email', label: 'Email', type: 'text', required: true, maxLength: 255, minLength: 8 },
        { name: 'phone', label: 'Phone Number', type: 'text', required: true, maxLength: 17, minLength: 16 },
    ];

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await profileAPI.getProfile();
                setFormData(response.data || {});
            } catch (error) {
                console.error('Error loading profile:', error);
                toast.error('Failed to load profile');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await profileAPI.updateProfile(formData);
            toast.success('Profile updated!');
            navigate('/');
        } catch (error) {
            setErrors(error.response?.data || {});
            toast.error('Update failed');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className='text-center p-5'>
                <Spinner animation='border' /><br />
                <span className='ms-2'>Loading...</span>
            </div>
        );
    }

    return (
        <Form onSubmit={handleSubmit}>
            <Row>
                {fields.map((field) => (
                    <Col md={6} key={field.name} className='mb-3'>
                        <Form.Group>
                            <Form.Label>{field.name}</Form.Label>
                            <Form.Control
                                type={field.type}
                                value={formData[field.name]}
                                onChange={(e) => setFormData({
                                    ...formData,
                                    [field]: e.target.value
                                })}
                                isInvalid={!!errors[field.name]}
                            />
                            <Form.Control.Feedback type='invalid'>
                                {errors[field.name]?.join(' ')}
                            </Form.Control.Feedback>
                        </Form.Group>
                    </Col>
                ))}
            </Row>
            <div className='text-center mt-4'>
                <Button variant='primary' type='submit' disabled={loading}>
                    {loading ? (
                        <>
                            <Spinner as='span' animation='border' size='sm' className='me-2' />
                            Loading...
                        </>
                    ) : 'Update Profile'}
                </Button>
            </div>
        </Form>
    );
};
