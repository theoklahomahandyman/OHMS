import { Container, Row, Col, Card } from 'react-bootstrap';
import LoginForm from '../components/profile/LoginForm';

function Login() {
    return (
        <div className='bg-gradient-primary min-vh-100 d-flex align-items-center'>
            <Container className='py-5'>
                <Row className='justify-content-center'>
                    <Col md={8} lg={6} xl={5}>
                        <Card className='shadow'>
                            <Card.Body className='p-4 p-md-5'>
                                <div className='text-center mb-3'>
                                    <i className='fas fa-tools fa-4x mb-3 text-primary'></i>
                                    <h1 className='h3 text-primary mb-4'>OHMS</h1>
                                    <h2 className='h5 text-muted'>OHMS Admin Login</h2>
                                </div>
                                <LoginForm />
                                <div className='text-center mt-3'>
                                    <a className='small text-decoration-none' href='/forgot-password'>Forgot Password?</a>
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default Login;
