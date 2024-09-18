import Page from '../components/reusable/Page';
import Form from '../components/reusable/Form';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';


function Password() {
    const route = '/user/';

    const navigate = useNavigate();

    const fields = [
        { name: 'password', label: 'Password', type: 'password', required: true, elementType: 'input', minLength: 10 },
        { name: 'confirm_password', label: 'Confirm Password', type: 'password', required: true, elementType: 'input', minLength: 10 },
    ];

    const handleSuccess = (data) => {
        toast.success('Password successfully updated!');
        navigate('/');
    }

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Password</h1>
            <p className="mb-4 text-center">Please use this page to update your password.</p>
            <Form fields={fields} method='patch' route={route} buttonText='Update Password' buttonStyle='success' onSuccess={handleSuccess} />
        </Page>
    )
}

export default Password;
