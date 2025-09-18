import { useState, useEffect } from 'react';
import { employeeAPI } from '../services/api';

export const useEmployees = (selectedDate) => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEmployees = async () => {
    setLoading(true);
    setError(null);

    try {
      let response;
      if (selectedDate) {
        // Fetch employees with records for specific date
        response = await employeeAPI.getEmployeesForDate(selectedDate);
      } else {
        // Fetch all employees with current status
        response = await employeeAPI.getAll();
      }
      
      setEmployees(response.employees || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching employees:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateEmployeeStatus = async (employeeId, status) => {
    try {
      await employeeAPI.updateStatus(employeeId, status);
      // Refresh employees after status update
      await fetchEmployees();
      return { success: true };
    } catch (err) {
      console.error('Error updating employee status:', err);
      return { success: false, message: err.message };
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, [selectedDate]);

  return {
    employees,
    loading,
    error,
    refetch: fetchEmployees,
    updateStatus: updateEmployeeStatus
  };
};
