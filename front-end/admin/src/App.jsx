import ProtectedRoute from './components/reusable/ProtectedRoute';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import Service from './pages/Service';
import Login from './pages/Login';

import 'react-toastify/ReactToastify.min.css';
import './styles/styles.min.css';

function App() {
  	return (
    	<>
			<BrowserRouter>
				<Routes>
					<Route path='/' element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
					<Route path='/service/' element={<ProtectedRoute><Service /></ProtectedRoute>}/>
					<Route path='/login/' element={<Login />} />
					<Route path='*' element={<NotFound />} />
				</Routes>
			</BrowserRouter>
			<ToastContainer />
    	</>
  	)
}

export default App;
