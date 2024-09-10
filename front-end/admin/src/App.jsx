import ProtectedRoute from './components/reusable/ProtectedRoute';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import Supplier from './pages/Supplier';
import Purchase from './pages/Purchase';
import Material from './pages/Material';
import Customer from './pages/Customer';
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

					<Route path='/customer/' element={<ProtectedRoute><Customer /></ProtectedRoute>} />

					<Route path='/service/' element={<ProtectedRoute><Service /></ProtectedRoute>} />

					<Route path='/supplier/' element={<ProtectedRoute><Supplier /></ProtectedRoute>} />

					<Route path='purchase' element={<ProtectedRoute><Purchase /></ProtectedRoute>} />

					<Route path='/material/' element={<ProtectedRoute><Material /></ProtectedRoute>} />

					<Route path='/login/' element={<Login />} />
					
					<Route path='*' element={<NotFound />} />
				</Routes>
			</BrowserRouter>
			<ToastContainer />
    	</>
  	)
}

export default App;
