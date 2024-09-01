import { REFRESH_TOKEN, ACCESS_TOKEN } from '../constants';
import { Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';
import Loading from './Loading';
import api from '../api';

const ProtectedRoute = ({ children }) => {
    const [isAuthorized, setIsAuthorized] = useState(null);

        useEffect(() => {
            const auth = async () => {
                const token = Cookies.get(ACCESS_TOKEN);

                if (!token) {
                    toast.warning('Please log in before accessing this page.');
                    setIsAuthorized(false);
                    return;
                }

                try {
                    const decoded = jwtDecode(token);
                    const tokenExpiration = decoded.exp;
                    const now = Date.now() / 1000;
                    if (tokenExpiration < now) {
                        await refreshToken();
                    } else {
                        setIsAuthorized(true);
                    }
                } catch {
                    toast.error('Session expired. Please log in again.');
                    setIsAuthorized(false);
                }
            };

            auth().catch(() => setIsAuthorized(false));
        }, []);

        const refreshToken = async () => {
            const refreshToken = Cookies.get(REFRESH_TOKEN);

            if (!refreshToken) {
                toast.error("Session expired. Please log in again.");
                setIsAuthorized(false);
                return;
            }

            try {
                const response = await api.post('/token/refresh/', { refresh: refreshToken });
                if (response.status === 200) {
                    Cookies.set(ACCESS_TOKEN, response.data.access);
                    setIsAuthorized(true);
                } else {
                    toast.error('Session expired. Please log in again.');
                    setIsAuthorized(false);
                }
            } catch {
                toast.error('Session expired. Please log in again.');
                setIsAuthorized(false);
            }
        };

        if (isAuthorized === null) {
            return <Loading />
        }

        return isAuthorized ? children : <Navigate to='/login/' />;
};

ProtectedRoute.propTypes = {
    children: PropTypes.node.isRequired
};

export default ProtectedRoute;
