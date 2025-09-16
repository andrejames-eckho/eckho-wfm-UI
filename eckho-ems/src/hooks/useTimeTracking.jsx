import { useState, useEffect } from 'react';
import { timeTrackingAPI } from '../services/api';

export const useTimeTracking = (employeeId) => {
  const [trackingData, setTrackingData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTrackingStatus = async () => {
    if (!employeeId) return;
    
    setLoading(true);
    setError(null);

    try {
      const data = await timeTrackingAPI.getStatus(employeeId);
      setTrackingData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching tracking status:', err);
    } finally {
      setLoading(false);
    }
  };

  const performTimeAction = async (action) => {
    if (!employeeId) return { success: false, message: 'No employee ID' };

    setLoading(true);
    setError(null);

    try {
      const response = await timeTrackingAPI.performAction(employeeId, action);
      
      if (response.success) {
        setTrackingData(response.data);
        return { success: true, message: response.message };
      } else {
        setError(response.message);
        return { success: false, message: response.message };
      }
    } catch (err) {
      const errorMessage = err.message || 'Time tracking action failed';
      setError(errorMessage);
      return { success: false, message: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const timeIn = () => performTimeAction('time_in');
  const timeOut = () => performTimeAction('time_out');
  const breakIn = () => performTimeAction('break_in');
  const breakOut = () => performTimeAction('break_out');

  useEffect(() => {
    fetchTrackingStatus();
  }, [employeeId]);

  return {
    trackingData,
    loading,
    error,
    timeIn,
    timeOut,
    breakIn,
    breakOut,
    refetch: fetchTrackingStatus
  };
};
