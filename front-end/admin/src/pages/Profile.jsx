import Page from '../components/reusable/Page';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';


function Profile() {
    const navigate = useNavigate();

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
            <Form fields={fields} method='patch' route='/user/' buttonText='Update Profile' buttonStyle='success' onSuccess={handleSuccess} />
        </Page>
    )
}

export default Profile;
