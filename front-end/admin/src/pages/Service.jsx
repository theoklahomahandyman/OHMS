import ServiceTable from '../components/service/ServiceTable';
import Page from '../components/reusable/Page';

function Service() {
    const heading = 'Service Types';
    const text = 'Service Types are used to classify the different service types available to be used in work orders. They are available to users when filling out the contact form to classify the general need of the job.';

    return (
        <Page heading={heading} text={text}>
            <ServiceTable />
        </Page>
    )
}

export default Service;
