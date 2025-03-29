import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import {makeRequest} from '../api';

function Purchase() {
    const [suppliers, setSuppliers] = useState([]);
    const [supplierAddresses, setSupplierAddresses] = useState([]);
    const [addresses, setAddresses] = useState([]);

    const heading = 'Purchases';

    const text = 'Purchases are acquisitions of materials from suppliers. They are used to increase inventory levels for materials.';

    useEffect(() => {
        async function fetchSuppliers() {
            try {
                const response = await makeRequest('get', '/supplier/');
                setSuppliers(response.data);
            } catch {
                toast.error('No Suppliers Found!');
            }
        }
        fetchSuppliers();
    }, []);

    useEffect(() => {
        const fetchAddresses = async () => {
            if (suppliers.length > 0) {
                const updatedAddresses = [];
                await Promise.all(suppliers.map(async (supplier) => {
                    try {
                        const response = await makeRequest('get', `/supplier/address/${supplier.id}/`);
                        updatedAddresses.push({
                            id: supplier.id,
                            ...response.data
                        });
                    } catch {
                        toast.error('No Addresses Found!');
                    }
                }));
                setSupplierAddresses(updatedAddresses);
            }
        };
        fetchAddresses();
    }, [suppliers]);


    const handleSupplierChange = async (event) => {
        const supplier = event.target.value;
        setAddresses([])
        if (supplier) {
            try {
                const response = await makeRequest('get', `/supplier/addresses/${supplier}`);
                setAddresses(response.data);
            } catch {
                toast.error('No Addresses Found!');
            }
        }
    }

    const relatedData = [
        {name: 'supplier', data: suppliers},
        {name: 'supplier_address', data: supplierAddresses},
    ];

    const fields = [
        {name: 'supplier', label: 'Supplier', required: true, elementType: 'select', data: suppliers.map(supplier => ({ value: supplier.id, label: supplier.name })), customChange: handleSupplierChange, route: 'supplier/name'},
        {name: 'supplier_address', label: 'Supplier Address', required: true, elementType: 'select', data: addresses.map(address => ({ value: address.id, label: `${address.street_address} ${address.city}, ${address.state} ${address.zip}` })), route: '/supplier/address'},
        {name: 'tax', label: 'Tax Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'total', label: 'Total Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'uploaded_images', label: 'Reciept', required: true, elementType: 'input', type: 'file'},
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Purchase' route='/purchase/' updateType='page' relatedData={relatedData} />
        </Page>
    )
}

export default Purchase;
