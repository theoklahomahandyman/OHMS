import PasswordForm from '../components/profile/PasswordForm';
import Page from '../components/reusable/Page';


function Password() {
    const heading = 'Password';
    const text = 'Please use this page to update your password.';

    return (
        <Page heading={heading} text={text}>
            <PasswordForm />
        </Page>
    );
};

export default Password;
