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
    const errorData = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
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
  }
};

// Time tracking API
export const timeTrackingAPI = {
  performAction: async (employeeId, action) => {
    const response = await fetch(`${API_BASE_URL}/time-tracking`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ employeeId, action })
    });
    return handleResponse(response);
  },

  getStatus: async (employeeId) => {
    const response = await fetch(`${API_BASE_URL}/time-tracking/${employeeId}`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
  },

  getRecords: async (employeeId, months = 3) => {
    const response = await fetch(`${API_BASE_URL}/time-records/${employeeId}?months=${months}`, {
      headers: getAuthHeaders()
    });
    return handleResponse(response);
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
