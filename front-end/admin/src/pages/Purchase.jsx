import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import api from '../api';

function Purchase() {
    const [suppliers, setSuppliers] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [materials, setMaterials] = useState([]);

    const heading = 'Purchases';

    const text = 'Purchases are acquisitions of materials from suppliers. They are used to increase inventory levels for materials.';

    useEffect(() => {
        async function fetchSuppliers() {
            try {
                const response = await api.get('/supplier/');
                setSuppliers(response.data);
            } catch {
                toast.error('No Suppliers Found!');
            }
        }
        fetchSuppliers();
    }, []);

    useEffect(() => {
        async function fetchMaterials() {
            try {
                const response = await api.get('/material/');
                setMaterials(response.data);
            } catch {
                toast.error('No Materials Found!');
            }
        }
        fetchMaterials();
    }, []);

    const handleSupplierChange = async (event) => {
        const supplier = event.target.value;
        setAddresses([])
        if (supplier) {
            try {
                const response = await api.get(`/supplier/addresses/${supplier}`);
                setAddresses(response.data);
            } catch {
                toast.error('No Addresses Found!');
            }
        }
    }

    const fields = [
        {name: 'supplier', label: 'Supplier', required: true, elementType: 'select', data: suppliers.map(supplier => ({ value: supplier.id, label: supplier.name })), customChange: handleSupplierChange, route: 'supplier/name'},
        {name: 'supplier_address', label: 'Supplier Address', required: true, elementType: 'select', data: addresses.map(address => ({ value: address.id, label: `${address.street_address} ${address.city}, ${address.state} ${address.zip}` })), route: '/supplier/address'},
        {name: 'tax', label: 'Tax Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'total', label: 'Total Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'reciept', label: 'Reciept', required: true, elementType: 'input', type: 'file', multiple: false, accept: 'image/*'},
    ];

    const materialFields = [
        {name: 'material', label: 'Material', required: true, elementType: 'select', data: materials.map(material => ({ value: material.id, label: material.name }))},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    const formsets = [
        {entity: 'Material', route: '/purchase/material/', fields: materialFields}
    ]

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Purchase' route='/purchase/' formsets={formsets} />
        </Page>
    )
}

export default Purchase;
