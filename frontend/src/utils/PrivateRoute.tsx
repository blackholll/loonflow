import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

interface PrivateRouteProps {
  element: React.ReactElement | null;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ element }) => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  console.log('routeisAuthenticated:', isAuthenticated);
  return isAuthenticated ? element : <Navigate to="/signin" />;
};

export default PrivateRoute;
