import PurchaseTable from '../components/purchase/PurchaseTable';
import Page from '../components/reusable/Page';

function Purchase() {
    const heading = 'Purchases';
    const text = 'Purchases are acquisitions of materials from suppliers. They are used to increase inventory levels for materials.';

    return (
        <Page heading={heading} text={text}>
            <PurchaseTable />
        </Page>
    )
}

export default Purchase;
