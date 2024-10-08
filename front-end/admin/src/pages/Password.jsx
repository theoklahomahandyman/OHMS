import Page from '../components/reusable/Page';
import Form from '../components/reusable/form/Form';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';


function Password() {
    const heading = 'Password';

    const text = 'Please use this page to update your password.';

    const route = '/user/';

    const navigate = useNavigate();

    const fields = [
        { name: 'password', label: 'Password', type: 'password', required: true, elementType: 'input', minLength: 10 },
        { name: 'confirm_password', label: 'Confirm Password', type: 'password', required: true, elementType: 'input', minLength: 10 },
    ];

    const handleSuccess = () => {
        toast.success('Password successfully updated!');
        navigate('/');
    }

    return (
        <Page heading={heading} text={text}>
            <Form fields={fields} method='patch' route={route} buttonText='Update Password' buttonStyle='success' onSuccess={handleSuccess} />
        </Page>
    )
}

export default Password;
