import ProtectedRoute from './components/reusable/ProtectedRoute';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import EditPurchase from './pages/EditPurchase';
import EditOrder from './pages/EditOrder';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import Supplier from './pages/Supplier';
import Purchase from './pages/Purchase';
import Material from './pages/Material';
import Customer from './pages/Customer';
import Password from './pages/Password';
import Service from './pages/Service';
import Profile from './pages/Profile';
import Order from './pages/Order';
import Admin from './pages/Admin';
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

					<Route path='/purchase/' element={<ProtectedRoute><Purchase /></ProtectedRoute>} />
					<Route path='/purchase/:id/' element={<ProtectedRoute><EditPurchase /></ProtectedRoute>} />

					<Route path='/material/' element={<ProtectedRoute><Material /></ProtectedRoute>} />

					<Route path='/order/' element={<ProtectedRoute><Order /></ProtectedRoute>} />
					<Route path='/order/:id/' element={<ProtectedRoute><EditOrder /></ProtectedRoute>} />

					<Route path='/password/' element={<ProtectedRoute><Password /></ProtectedRoute>} />

					<Route path='/profile/' element={<ProtectedRoute><Profile /></ProtectedRoute>} />

					<Route path='/admin/' element={<ProtectedRoute><Admin /></ProtectedRoute>} />

					<Route path='/login/' element={<Login />} />

					<Route path='*' element={<NotFound />} />
				</Routes>
			</BrowserRouter>
			<ToastContainer />
    	</>
  	)
}

export default App;
