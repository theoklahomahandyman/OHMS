import ProfileForm from '../components/profile/ProfileForm';
import Page from '../components/reusable/Page';

function Profile() {
    const heading = 'Profile';
    const text = 'Please use this page to update your profile information.';

    return (
        <Page heading={heading} text={text}>
            <ProfileForm />
        </Page>
    );
};

export default Profile;
