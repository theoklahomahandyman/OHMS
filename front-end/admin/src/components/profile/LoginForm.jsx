import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../constants';
import { Form, Button, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import { profileAPI } from '../../api';
import { useState } from 'react';
import Cookies from 'js-cookie';

export default function LoginForm() {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await profileAPI.login(formData);
            Cookies.set(ACCESS_TOKEN, data.access);
            Cookies.set(REFRESH_TOKEN, data.refresh);
            navigate('/');
            toast.success('Welcome!');
        } catch (error) {
            console.error(error);
            setErrors(error.response?.data || {});
            toast.error('Email or password incorrect, please try again!');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className='mb-3'>
                <Form.Label>Email Address</Form.Label>
                <Form.Control
                    type='email'
                    required
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    isInvalid={!!errors.email}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.email?.join(' ')}
                </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className='mb-3'>
                <Form.Label>Password</Form.Label>
                <Form.Control
                    type='password'
                    required
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    isInvalid={!!errors.password}
                />
                <Form.Control.Feedback type='invalid'>
                    {errors.password?.join(' ')}
                </Form.Control.Feedback>
            </Form.Group>
            <div className='text-center'>
                <Button variant='primary' type='submit' disabled={loading} className='w-100'>
                    {loading ? (
                        <>
                            <Spinner as='span' animation='border' size='sm' className='me-2' /><br />
                            Logging in...
                        </>
                    ) : 'Login'}
                </Button>
            </div>
        </Form>
    );
};
