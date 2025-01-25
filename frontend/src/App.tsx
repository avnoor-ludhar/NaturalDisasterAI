import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css'
import { useAppDispatch, useAppSelector } from './redux/store';
import { addUser, removeUser } from "@/redux/features/userSlice";
import { useEffect, useState } from 'react';
import api from './lib/axios';
import HomePage from './pages/HomePage';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Navbar from './components/navbar';
import { LoaderCircle } from 'lucide-react';
import DisasterForm from './pages/PeopleForm';
import DisasterView from './pages/ViewPosts';
import PreviousDisaster from './pages/PreviousDisaster';

type userType = {
  email: string,
  token: string
}

function App() {
  const dispatch = useAppDispatch();
  const user = useAppSelector(state => state.user.user);
  const [isUserChecked, setIsUserChecked] = useState(false);
  // const location = useLocation();

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await api.get("/api/user/session");
        const user: userType = { token: response.data.token, email: response.data.email };
        dispatch(addUser(user));
      } catch (error) {
        console.error("No active session or invalid token");
        dispatch(removeUser());
      } finally {
        setIsUserChecked(true);
      }
    };
    checkSession();
  }, [dispatch]);


  if (!isUserChecked) {
    return <div className="flex justify-center items-center h-screen">
      <LoaderCircle className="animate-spin pr-2" />
      Loading...
    </div>;
  }

  return (
    <Router>
        <div className="min-h-screen h-fit bg-gray-100">
          <Navbar />
          <Routes>
            <Route path='/login' element={!user ? <Login /> : <Navigate to='/home' />} />
            <Route path='/' element={!user ? <Login /> : <Navigate to='/home' />} />
            <Route path='/signup' element={!user ? <SignUp /> : <Navigate to='/home' />} />
            <Route path='/home' element={user ? <HomePage /> : <Navigate to='/login' />} />
            <Route path='/disaster-form' element={user ? <DisasterForm/> : <Navigate to='/login' />} />
            <Route path='/disaster-view' element={user ? <DisasterView/> : <Navigate to='/login' />} />
            <Route path='/prev-data' element={user ? <PreviousDisaster/> : <Navigate to='/login' />} />
          </Routes>
        </div>
    </Router>
  )
}

export default App;
