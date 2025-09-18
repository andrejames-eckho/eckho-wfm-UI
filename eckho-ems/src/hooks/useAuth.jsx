import { useState, useEffect, createContext, useContext } from 'react';
import { authAPI, authHelpers } from '../services/api';

// Create Auth Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('eckho_authenticated') === 'true';
  });
  
  const [userType, setUserType] = useState(() => {
    return localStorage.getItem('eckho_user_type') || 'admin';
  });
  
  const [currentEmployee, setCurrentEmployee] = useState(() => {
    const savedEmployee = localStorage.getItem('eckho_current_employee');
    return savedEmployee ? JSON.parse(savedEmployee) : null;
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Save auth state to localStorage
  useEffect(() => {
    localStorage.setItem('eckho_authenticated', isAuthenticated.toString());
  }, [isAuthenticated]);

  useEffect(() => {
    localStorage.setItem('eckho_user_type', userType);
  }, [userType]);

  useEffect(() => {
    if (currentEmployee) {
      localStorage.setItem('eckho_current_employee', JSON.stringify(currentEmployee));
    } else {
      localStorage.removeItem('eckho_current_employee');
    }
  }, [currentEmployee]);

  const login = async (username, password) => {
    setLoading(true);
    setError(null);

    try {
      const response = await authAPI.login(username, password);
      
      if (response.success) {
        // Store auth token
        authHelpers.setToken(response.token);
        
        // Update auth state
        setIsAuthenticated(true);
        setUserType(response.user_type);
        
        if (response.user_type === 'employee' && response.employee_id) {
          // For employees, we'll fetch their data from the backend
          setCurrentEmployee({ id: response.employee_id });
        } else {
          setCurrentEmployee(null);
        }

        return { success: true, userType: response.user_type, employeeId: response.employee_id };
      } else {
        setError(response.message);
        return { success: false, message: response.message };
      }
    } catch (err) {
      const errorMessage = err.message || 'Login failed';
      setError(errorMessage);
      return { success: false, message: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Clear auth token
    authHelpers.removeToken();
    
    // Clear auth state
    setIsAuthenticated(false);
    setUserType('admin');
    setCurrentEmployee(null);
    setError(null);
    
    // Clear localStorage
    localStorage.removeItem('eckho_authenticated');
    localStorage.removeItem('eckho_user_type');
    localStorage.removeItem('eckho_current_employee');
    localStorage.removeItem('eckho_selected_date');
  };

  const value = {
    isAuthenticated,
    userType,
    currentEmployee,
    loading,
    error,
    login,
    logout,
    setCurrentEmployee
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
