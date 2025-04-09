import { Form, Button, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router';
import { profileAPI } from '../../api';
import { toast } from 'react-toastify';
import { useState } from 'react';

export default function PasswordForm() {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await profileAPI.changePassword(formData);
            toast.success('Password changed successfully!');
            navigate('/');
        } catch (error) {
            setErrors(error.response?.data || {});
            toast.error('Failed to change password');
        } finally {
            setLoading(false);
        }
    };

    if (formData.password !== formData.confirm_password) {
        setErrors({ confirm_password: ['Passwords do not match']});
        return;
    }

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className='mb-3'>
                <Form.Label>Password</Form.Label>
                <Form.Control
                    type='password'
                    required
                    minLength={10}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
            </Form.Group>
            <Form.Group className='mb-3'>
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                    type='password'
                    required
                    minLength={10}
                    onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                    isInvalid={!!errors.confirm_password}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.password?.join(' ')}
                </Form.Control.Feedback>
            </Form.Group>
            <div className='text-center'>
                <Button variant='success' type='submit' disabled={loading}>
                    {loading ? (
                        <>
                            <Spinner as='span' animation='border' size='sm' className='me-2' /><br />
                            Updating...
                        </>
                    ) : 'Change Password' }
                </Button>
            </div>
        </Form>
    );
};
