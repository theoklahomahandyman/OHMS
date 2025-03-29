import { Table, Spinner, Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import $ from 'jquery';

export default function InventoryTable({ apiFunc, fields, extraFields }) {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiFunc();
                setData(response.data);
            } catch (error) {
                console.error('Error loading inventory data:', error);
                setError('Failed to load inventory data');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [apiFunc]);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0) {
            setTimeout(() => {
                $('#dataTable').DataTable();
            }, 1);
        }
    }, [data]);

    if (loading) {
        return (
            <div className='text-center my-5'>
                <Spinner animation='border' role='status'>
                    <span className='visually-hidden'>Loading...</span>
                </Spinner>
            </div>
        );
    }

    if (error) {
        return <Alert variant='danger' className='my-4'>{error}</Alert>;
    }

    const allFields = [...fields, ...extraFields];

    return (
        <div className='mt-4'>
            <Table striped bordered hover responsive className='shadow-sm'>
                <thead className='bg-light'>
                    <tr>
                        {allFields.map((field) => (
                            <th key={field.name} className='py-3'>{field.label}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.id}>
                            {allFields.map((field) => (
                                <td key={`${item.id}-${field.name}`} className='py-2'>
                                    {field.name === 'unit_cost' ? `$${item[field.name]}` : item[field.name]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

InventoryTable.propTypes = {
    apiFunc: PropTypes.func.isRequired,
    fields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired
    })).isRequired,
    extraFields: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string,
        label: PropTypes.string
    }))
};
