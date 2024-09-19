import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import api from '../api';

function Order() {
    const [customers, setCustomers] = useState([]);
    const [services, setServices] = useState([]);

    const calloutChoices = [
        { value: '50.0', label: 'Standard - $50.00' },
        { value: '175.0', label: 'Emergency - $175.00' }
    ];

    useEffect(() => {
        async function fetchCustomers() {
            try {
                const response = await api.get('/customer/');
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
                const response = await api.get('/service/');
                setServices(response.data);
            } catch {
                toast.error('No Services Found!');
            }
        }
        fetchServices();
    }, []);

    const fields = [
        {name: 'customer', label: 'Customer', required: true, elementType: 'select', data: customers.map(customer => ({ value: customer.id, label: `${customer.first_name} ${customer.last_name}` })), route: '/customer/name'},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 2000},
        {name: 'service', label: 'Service', required: true, elementType: 'select', data: services.map(service => ({ value: service.id, label: service.name })), route: '/service/name'},
        {name: 'hourly_rate', label: 'Hourly Rate', required: false, elementType: 'input', type: 'number', minValue: 75.0},
        {name: 'hours_worked', label: 'Hours Worked', required: false, elementType: 'input', type: 'number', minValue: 3.0},
        {name: 'material_upcharge', label: 'Material Upcharge', required: false, elementType: 'input', type: 'number', minValue: 15.0, maxValue: 75.0},
        {name: 'tax', label: 'Tax', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 20.0},
        {name: 'total', label: 'Total', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'completed', label: 'Complete', required: false, elementType: 'input', type: 'checkbox'},
        {name: 'paid', label: 'Paid', required: false, elementType: 'input', type: 'checkbox'},
        {name: 'discount', label: 'Discount', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 100.0},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 10000},
        {name: 'callout', label: 'Callout Type', required: false, elementType: 'select', data: calloutChoices},
    ];

    const costFields = [
        {name: 'name', label: 'Name', type: 'text', required: true, elementType: 'input', minLength: 2, maxLength: 300},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input', minValue: 0.0},
    ];

    const formsets = [
        {entity: 'Line Item Cost', route: '/order/cost/', fields: costFields}
    ]

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Work Orders</h1>
            <p className="mb-4 text-center">
                Work orders are either estimates, or projects whether complete or not.
            </p>
            <Table fields={fields} name='Work Order' route='/order/' formsets={formsets} />
        </Page>
    )
}

export default Order;
