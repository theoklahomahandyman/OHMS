import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import makeRequest from '../api';

function Order() {
    const [customers, setCustomers] = useState([]);
    const [services, setServices] = useState([]);

    const heading = 'Work Orders';

    const text = 'Work orders are either estimates or projects whether they are complete or not.';

    const calloutChoices = [
        { value: '50.0', label: 'Standard - $50.00' },
        { value: '175.0', label: 'Emergency - $175.00' },
    ];

    useEffect(() => {
        async function fetchCustomers() {
            try {
                const response = await makeRequest('get', '/customer/');
                setCustomers(response.data);
            } catch {
                toast.error('No Customers Found!');
            }
        }
        fetchCustomers();
    }, []);

    useEffect(() => {
        async function fetchServices() {
            try {
                const response = await makeRequest('get', '/service/');
                setServices(response.data);
            } catch {
                toast.error('No Services Found!');
            }
        }
        fetchServices();
    }, []);

    const relatedData = [
        {name: 'customer', data: customers},
        {name: 'service', data: services},
    ];

    const fields = [
        {name: 'customer', label: 'Customer', required: true, elementType: 'select', data: customers.map(customer => ({ value: customer.id, label: `${customer.first_name} ${customer.last_name}` })), route: '/customer/name'},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'service', label: 'Service', required: true, elementType: 'select', data: services.map(service => ({ value: service.id, label: service.name })), route: '/service/name'},
        {name: 'completed', label: 'Complete', required: false, elementType: 'input', type: 'checkbox', disabled: true},
        {name: 'paid', label: 'Paid', required: false, elementType: 'input', type: 'checkbox', disabled: true},
        {name: 'discount', label: 'Discount (%)', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 100.0},
        {name: 'discount_total', label: 'Discount Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'callout', label: 'Callout Type', required: false, elementType: 'select', data: calloutChoices},
        {name: 'uploaded_images', label: 'Pictures', required: false, elementType: 'input', type: 'file'},
        {name: 'hourly_rate', label: 'Hourly Rate ($)', required: false, elementType: 'input', type: 'number', minValue: 75.0},
        {name: 'hours_worked', label: 'Hours Worked', required: false, elementType: 'input', type: 'number', minValue: 3.0, disabled: true},
        {name: 'labor_total', label: 'Labor Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'line_total', label: 'Line Item Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'material_upcharge', label: 'Material Upcharge (%)', required: false, elementType: 'input', type: 'number', minValue: 15.0, maxValue: 75.0},
        {name: 'material_total', label: 'Material Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'tax', label: 'Tax (%)', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 20.0},
        {name: 'tax_total', label: 'Tax Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'subtotal', label: 'Subtotal ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'total', label: 'Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'payment_total', label: 'Payment Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'working_total', label: 'Total Due ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 2000},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 10000},
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Work Order' route='/order/' updateType='page' relatedData={relatedData} />
        </Page>
    )
}

export default Order;
