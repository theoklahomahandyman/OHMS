import { ToastContainer } from 'react-toastify';
import Home from './pages/Home';

import 'react-toastify/ReactToastify.min.css';
import './styles/styles.min.css';

function App() {
    return (
        <>
            <Home />
            <ToastContainer />
        </>
    )
}

export default App
