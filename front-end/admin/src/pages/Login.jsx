import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import Form from '../components/reusable/Form';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import Cookies from 'js-cookie';

function Login() {
    const navigate = useNavigate();

    const customError = 'Email or password incorrect, please try again!';

    const fields = [
        {name: 'email', label: 'Email Address', type: 'email', elementType: 'input', required: true},
        {name: 'password', label: 'Password', type: 'password', elementType: 'input', required: true}
    ]

    const handleSuccess = (data) => {
        Cookies.set(ACCESS_TOKEN, data.access);
        Cookies.set(REFRESH_TOKEN, data.refresh);
        navigate('/');
        setTimeout(() => {
            toast.success('Welcome!');
        }, 500);
    }

    return (
        <div className="bg-gradient-primary min-vh-100 d-flex align-items-center justify-content-center">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-lg-6 col-md-8">
                        <div className="card o-hidden border-0 shadow-lg my-5">
                            <div className="card-body p-0">
                                <div className="text-center p-5">
                                    <i className="fas fa-tools fa-4x mb-3 text-primary"></i>
                                    <h1 className="h3 text-primary mb-4">OHMS</h1>
                                    <h1 className="h4 text-gray-900 mb-4">OHMS Admin Login</h1>
                                    <Form fields={fields} method='post' route='/user/login/' buttonText='Login' buttonStyle='primary' onSuccess={handleSuccess} customError={customError} />
                                    <hr />
                                    <div className="text-center">
                                        <a className="small" href="forgot-password.html">Forgot Password?</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
