import PropTypes from 'prop-types';
import CreateModal from './CreateModal';

function Table({ name, fields, route }) {

    return (
        <div>
            <div className="card shadow mb-4">
                <div className="card-header py-3 d-flex justify-content-between align-items-center">
                    <h6 className="m-0 font-weight-bold text-primary">{name}s</h6>
                    <CreateModal name={name} fields={fields} route={route}/>
                </div>
                <div className="card-body">
                    <div className="table-responsive">
                        <table className="table table-bordered" id="dataTable" width="100%" cellSpacing="0">
                            <thead>
                                <tr className='text-center'>
                                    {fields.map((field, index) => (
                                        <th key={index}>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                    ))}
                                    <th>Edit</th>
                                    <th>Delete</th>
                                </tr>
                            </thead>
                            <tfoot>
                                <tr className='text-center'>
                                    {fields.map((field, index) => (
                                        <th key={index}>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                    ))}
                                    <th>Edit</th>
                                    <th>Delete</th>
                                </tr>
                            </tfoot>
                            <tbody>
                                <tr className='text-center'>
                                    <td>Test Service</td>
                                    <td>Description of test service.</td>
                                    <td><button className="btn btn-primary">Edit</button></td>
                                    <td><button className="btn btn-danger">Delete</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
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
