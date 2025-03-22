import { Spinner } from 'react-bootstrap';

function Loading() {
    return (
        <div className="text-center">
            <Spinner animation="border" role="status" variant="light">
                <span className="sr-only">Loading...</span>
            </Spinner>
        </div>
    );
}

export default Loading;
