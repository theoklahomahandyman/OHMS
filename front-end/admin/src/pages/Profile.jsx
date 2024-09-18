import Loading from '../components/reusable/Loading';
import Page from '../components/reusable/Page';
import Form from '../components/reusable/Form';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import api from '../api';


function Profile() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});

    const route = '/user/';

    const navigate = useNavigate();

    useEffect(() => {
        console.log('useEffect is running');
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await api.get(route);
                console.log(response.data);
                setData(response.data || {});
            } catch (error) {
                console.log('Error fetching data:', error);
                setData({});
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);


    const fields = [
        { name: 'first_name', label: 'First Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2 },
        { name: 'last_name', label: 'Last Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2 },
        { name: 'email', label: 'Email', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 8 },
        { name: 'phone', label: 'Phone Number', type: 'text', required: true, elementType: 'input', maxLength: 17, minLength: 16 },
    ];

    const handleSuccess = (data) => {
        toast.success('Profile successfully updated!');
        navigate('/');
    }

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Profile</h1>
            <p className="mb-4 text-center">Please use this page to update your profile information.</p>
            {loading ? <Loading /> : (
                <Form fields={fields} method='patch' route={route} buttonText='Update Profile' buttonStyle='success' onSuccess={handleSuccess} initialData={data} />
            )}
        </Page>
    )
}

export default Profile;
