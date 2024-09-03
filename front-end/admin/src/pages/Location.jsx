import { useEffect, useState, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useParams } from 'react-router-dom';
import api from '../api';

function Location() {
    const { supplier_id } = useParams();
    const [supplier, setSupplier] = useState(null);

    const fetchSupplier = useCallback(async () => {
        try {
            const response = await api.get(`/supplier/${supplier_id}/`);
            setSupplier(response.data);
        } catch {
            setSupplier(null);
        }
    }, [supplier_id]);

    useEffect(() => {
        fetchSupplier();
    }, [fetchSupplier]);

    if (!supplier) {
        return <Loading />;
    }

    const fields = [
        {name: 'street_address', label: 'Street Address', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'city', label: 'City', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'state', label: 'State', type: 'text', required: true, maxLength: 13, minLength: 2},
        {name: 'zip', label: 'Zip Code', type: 'number', required: true },
        {name: 'notes', label: 'Notes', type: 'text', required: false, maxLength: 500 },
    ];

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Supplier Locations for {supplier.name}</h1>
            <p className="mb-4 text-center">
                Supplier locations are the physical locations where materials used in work orders are picked up and must be specified in an order.
            </p>
            <Table fields={fields} name='Location' route={`/supplier/addresses/${supplier_id}/`} />
        </Page>
    )
}

export default Location;
