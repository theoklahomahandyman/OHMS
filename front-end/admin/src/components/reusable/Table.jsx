import { useState, useEffect } from 'react';
import CreateModal from './CreateModal';
import PropTypes from 'prop-types';
import Loading from './Loading';
import api from '../../api';

function Table({ name, fields, route }) {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await api.get(route);
                setData(response.data || []);
            } catch {
                setData([]);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [route]);

    return (
        <div>
            <div className="card shadow mb-4">
                <div className="card-header py-3 d-flex justify-content-between align-items-center">
                    <h6 className="m-0 font-weight-bold text-primary">{name}s</h6>
                    <CreateModal name={name} fields={fields} route={route}/>
                </div>
                <div className="card-body">
                    {loading ? <Loading /> : (
                        <div className="table-responsive">
                            <table className="table table-bordered" id="dataTable" width="100%" cellSpacing="0">
                                <thead>
                                    <tr className='text-center'>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-header`}>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                        ))}
                                        <th>Edit</th>
                                        <th>Delete</th>
                                    </tr>
                                </thead>
                                <tfoot>
                                    <tr className='text-center'>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-footer`}>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                        ))}
                                        <th>Edit</th>
                                        <th>Delete</th>
                                    </tr>
                                </tfoot>
                                <tbody>
                                    {Array.isArray(data) && data.length > 0 ? (
                                        data.map((item) => (
                                            <tr className="text-center" key={`${item.pk}-${item.name}`}>
                                                {fields.map((field, index) => (
                                                    <td key={`${field.name}-${index}-${item.pk}`}>{item[field.name]}</td>
                                                ))}
                                                <td key={`edit-${item.id}`}><button className="btn btn-primary">Edit</button></td>
                                                <td key={`delete-${item.id}`}><button className="btn btn-danger">Delete</button></td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr className="text-center">
                                            <td className="text-center" colSpan={fields.length + 2}>No Data Yet</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

Table.propTypes = {
    name: PropTypes.string.isRequired,
    fields: PropTypes.array.isRequired,
    route: PropTypes.string.isRequired,
}

export default Table;
