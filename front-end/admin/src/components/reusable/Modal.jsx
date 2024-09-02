import PropTypes from 'prop-types';

import '../../styles/modal.css';

function Modal({ visible, onClose, title, children, size='' }) {
    if (!visible) return null;

    const handleClose = (event) => {
        if (event.target.id === 'wrapper') onClose();
    };

    return (
        <div className={`modal fade show ${size}`} id='wrapper' style={{ display: 'block'}} onClick={handleClose}>
            <div className={`modal-dialog ${size} modal-dialog-centered`}>
                <div className='modal-content'>
                    <div className='modal-header'>
                    <h5 className='modal-title'></h5>
                        <h1 className='modal-title text-center'>{title}</h1>
                        <button type='button' className='btn btn-danger ml-2' aria-label='Close' onClick={onClose}>X</button>
                    </div>
                    <div className="modal-body">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    )
}

Modal.propTypes = {
    visible: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    children: PropTypes.node.isRequired,
    size: PropTypes.string,
}

export default Modal;
