import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import Loading from '../components/Loading';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import { useState } from 'react';
import Cookies from 'js-cookie';
import api from '../api';

function Login() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({email: '', password: ''});

    const navigate = useNavigate();

    const login = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await api.post('/user/login/', data);
            Cookies.set(ACCESS_TOKEN, response.data.access);
            Cookies.set(REFRESH_TOKEN, response.data.refresh);
            setData({email: '', password: ''});
            setLoading(false);
            navigate('/');
            setTimeout(() => {
                toast.success('Welcome!');
            }, 500);
        } catch {
            setLoading(false);
            toast.warning('Incorrect email or password. Please try again!');
        }
    }

    const handleChange = (event) => {
        const { id, value } = event.target;
        setData(prevData => ({
            ...prevData,
            [id]: value
        }));
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
                                    {loading ? <Loading /> : (
                                        <div>
                                            <form className="user">
                                                <div className="form-group">
                                                    <input type="email" className="form-control form-control-user" id="email" value={data.email} onChange={handleChange} aria-describedby="emailHelp" placeholder="Enter Email Address..."/>
                                                </div>
                                                <div className="form-group">
                                                    <input type="password" className="form-control form-control-user" id="password" value={data.password} onChange={handleChange} placeholder="Enter Password..."/>
                                                </div>
                                                <button type="submit" className="btn btn-primary btn-user btn-block" id="loginButton" onClick={login}>Login</button>
                                            </form>
                                            <hr />
                                            <div className="text-center">
                                                <a className="small" href="forgot-password.html">Forgot Password?</a>
                                            </div>
                                        </div>
                                    )}
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
