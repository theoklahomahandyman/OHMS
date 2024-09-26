import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Service() {
    const heading = 'Service Types';

    const text = 'Service Types are used to classify the different service types available to be used in work orders. They are available to users when filling out the contact form to classify the general need of the job.';

    const fields = [
        {name: 'name', label: 'Service Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Service Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Service Type' route='/service/' />
        </Page>
    )
}

export default Service;
