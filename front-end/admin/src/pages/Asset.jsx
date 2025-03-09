import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Asset() {
    const heading = 'Assets';

    const text = 'Assets are machinary purchased and when used in an order incurs an hourly usage charge.';

    const fields = [
        {name: 'name', label: 'Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Asset' route='/inventory/asset/' updateType='page' />
        </Page>
    )
}

export default Asset;
