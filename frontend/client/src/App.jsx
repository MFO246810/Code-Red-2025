import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Home from './pages/Home';
import Account from './pages/Account';
import AddLog from './pages/AddLog';
import MyLogs from './pages/MyLogs';
import LogDetail from './pages/LogDetail';
import ProtectedRoute from './components/Protected_Route';
import CommunityLogs from './pages/Community_Logs';

function AppRoutes() {
  const location = useLocation();
  const hideLayout = location.pathname === "/login" || location.pathname === "/signup";

  if (hideLayout) {
    // Pages without layout
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
    );
  }

  // Pages with layout
  return (
    <Layout onLogout={null}>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/account" element={<ProtectedRoute><Account /></ProtectedRoute>} />
        <Route path="/add-log" element={<ProtectedRoute><AddLog /></ProtectedRoute>} />
        <Route path="/my-logs" element={<ProtectedRoute><MyLogs /></ProtectedRoute>} />
        <Route path="/log/:id" element={<ProtectedRoute><LogDetail /></ProtectedRoute>} />
        <Route path="/community-logs" element={<ProtectedRoute> <CommunityLogs /> </ProtectedRoute>} />
        <Route path="/forum" element={<div>Forum Page</div>} />
        <Route path="/laika" element={<div>Laika Page</div>} />
      </Routes>
    </Layout>
  );
}

function App() {

  return (
    <div className='app-container'>
    <Router>
      <AppRoutes/>
    </Router>
    </div>
  );
}

export default App;