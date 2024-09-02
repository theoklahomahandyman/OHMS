import Table from './reusable/Table';
import Modal from './reusable/Modal';
import PropTypes from 'prop-types';
import { useState } from 'react';

function LocationsModal({ id }) {
    const [visible, setVisible] = useState(false);

    const fields = [
        {name: 'street_address', label: 'Street Address', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'city', label: 'City', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'state', label: 'State', type: 'text', required: true, maxLength: 13, minLength: 2},
        {name: 'zip', label: 'Zipcode', type: 'number', required: true },
        {name: 'notes', label: 'Notes', type: 'text', required: false, maxLength: 500 },
    ];

    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-info action-btn'>Manage Locations</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title='Supplier Locations'>
                <Table fields={fields} name='Supplier Location' route={`/supplier/addresses/${id}/`} />
            </Modal>
        </>
    )
}

LocationsModal.propTypes = {
    id: PropTypes.number.isRequired,
}

export default LocationsModal;
