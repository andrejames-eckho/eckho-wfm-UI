const API_BASE_URL = 'http://localhost:8000/api';

// Helper function to get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('eckho_auth_token');
};

// Helper function to create headers with auth token
const getAuthHeaders = () => {
  const token = getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch (e) {
      errorData = { 
        detail: response.statusText || 'Network error',
        status: response.status
      };
    }
    
    const error = new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    error.status = response.status;
    error.data = errorData;
    
    // Handle specific error statuses
    if (response.status === 401) {
      // Unauthorized - clear auth and redirect to login
      authHelpers.removeToken();
      window.location.href = '/login';
    } else if (response.status === 403) {
      error.message = 'You do not have permission to perform this action';
    } else if (response.status >= 500) {
      error.message = 'Server error. Please try again later.';
    }
    
    throw error;
  }
  
  // For 204 No Content responses
  if (response.status === 204) {
    return {};
  }
  
  return response.json();
};

// Authentication API
export const authAPI = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    return handleResponse(response);
  }
};

// Employee API
export const employeeAPI = {
  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/employees`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/employees/${id}`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  updateStatus: async (id, status) => {
    const response = await fetch(`${API_BASE_URL}/employees/${id}/status`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ employeeId: id, status })
    });
    return handleResponse(response);
  },

  getEmployeesForDate: async (date) => {
    const response = await fetch(`${API_BASE_URL}/employees/date-records`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ startDate: date.toISOString() })
    });
    return handleResponse(response);
  },

  updateEmployee: async (id, employeeData) => {
    const response = await fetch(`${API_BASE_URL}/employees/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(employeeData)
    });
    return handleResponse(response);
  },

  create: async (employeeData) => {
    const response = await fetch(`${API_BASE_URL}/employees`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(employeeData)
    });
    return handleResponse(response);
  }
};

// Time tracking API
export const timeTrackingAPI = {
  performAction: async (employeeId, action) => {
    try {
      const response = await fetch(`${API_BASE_URL}/time-tracking`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ employeeId, action })
      });
      return await handleResponse(response);
    } catch (error) {
      console.error(`Error performing time tracking action ${action}:`, error);
      throw error;
    }
  },

  getStatus: async (employeeId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/time-tracking/${employeeId}`, {
        headers: getAuthHeaders()
      });
      return await handleResponse(response);
    } catch (error) {
      if (error.status !== 404) { // Don't log 404s as they're expected for new employees
        console.error(`Error getting time tracking status for employee ${employeeId}:`, error);
      }
      throw error;
    }
  },

  getRecords: async (employeeId, months = 3) => {
    try {
      const response = await fetch(`${API_BASE_URL}/time-records/${employeeId}?months=${months}`, {
        headers: getAuthHeaders()
      });
      return await handleResponse(response);
    } catch (error) {
      console.error(`Error getting time records for employee ${employeeId}:`, error);
      throw error;
    }
  }
};

// Dashboard API
export const dashboardAPI = {
  getSummary: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard/summary`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  getStatusColors: async () => {
    const response = await fetch(`${API_BASE_URL}/status-colors`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  }
};

// Auth helpers
export const authHelpers = {
  setToken: (token) => {
    localStorage.setItem('eckho_auth_token', token);
  },

  removeToken: () => {
    localStorage.removeItem('eckho_auth_token');
  },

  isAuthenticated: () => {
    return !!getAuthToken();
  }
};
