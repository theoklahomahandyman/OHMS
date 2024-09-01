import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Service() {

    const fields = [
        {name: 'name', label: 'Service Name', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'description', label: 'Service Description', type: 'text', required: false, maxLength: 500, minLength: 0}
    ];

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Service Types</h1>
            <p className="mb-4 text-center">
                Service Types are used to classify the different service types available to be used in work orders.
                They are available to users when filling out the contact form to classify the general need of the job.
            </p>
            <Table fields={fields} name='Service Type' route='/service/' />
        </Page>
    )
}

export default Service;
