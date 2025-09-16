import React, { useState, useEffect } from 'react'
import { Clock, Coffee, LogOut, User } from 'lucide-react'
import { useAuth } from '../hooks/useAuth.jsx'
import { useTimeTracking } from '../hooks/useTimeTracking.jsx'

export default function EmployeeDashboard({ employee, onSignOut }) {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [message, setMessage] = useState('')
  const { currentEmployee } = useAuth()
  
  // Use the employee ID from auth or props
  const employeeId = currentEmployee?.id || employee?.id
  
  const {
    trackingData,
    loading,
    error,
    timeIn,
    timeOut,
    breakIn,
    breakOut,
    refetch
  } = useTimeTracking(employeeId)

  // Update current time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const handleTimeAction = async (action, actionFunction) => {
    const result = await actionFunction()
    if (result.success) {
      setMessage(result.message)
      setTimeout(() => setMessage(''), 3000)
    } else {
      setMessage(`Error: ${result.message}`)
      setTimeout(() => setMessage(''), 5000)
    }
  }

  const handleTimeIn = () => handleTimeAction('Time In', timeIn)
  const handleTimeOut = () => handleTimeAction('Time Out', timeOut)
  const handleBreakIn = () => handleTimeAction('Break In', breakIn)
  const handleBreakOut = () => handleTimeAction('Break Out', breakOut)

  const getStatusColor = (status) => {
    const colors = {
      'Not Started': 'bg-gray-600',
      'On Duty': 'bg-green-500',
      'On Break': 'bg-yellow-500',
      'Completed': 'bg-blue-500'
    }
    return colors[status] || 'bg-gray-600'
  }

  const canTimeIn = !trackingData?.timeIn
  const canTimeOut = trackingData?.timeIn && !trackingData?.timeOut && trackingData?.status !== 'On Break'
  const canBreakIn = trackingData?.timeIn && !trackingData?.timeOut && !trackingData?.breakIn
  const canBreakOut = trackingData?.breakIn && !trackingData?.breakOut

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-800">
        <div className="flex items-center space-x-3">
          <Clock className="w-8 h-8 text-white" />
          <h1 className="text-xl font-semibold">ECKHO Employee Portal</h1>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <User className="w-5 h-5 text-gray-400" />
            <span className="text-sm text-gray-300">
              {employee.firstName} {employee.lastName}
            </span>
          </div>
          <button
            onClick={onSignOut}
            className="flex items-center space-x-2 px-3 py-2 bg-red-600 hover:bg-red-700 border border-red-500 rounded-md transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {/* Welcome Section */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-2">
            Welcome, {employee?.firstName || currentEmployee?.firstName}!
          </h2>
          <p className="text-lg text-gray-400">
            Manage your time tracking for today
          </p>
          <div className="mt-4 text-sm text-gray-500">
            Current Time: {currentTime.toLocaleTimeString('en-US', { 
              hour: 'numeric', 
              minute: '2-digit', 
              second: '2-digit',
              hour12: true 
            })}
          </div>
          {message && (
            <div className={`mt-4 p-3 rounded-md ${
              message.startsWith('Error') 
                ? 'bg-red-900/50 border border-red-500 text-red-200' 
                : 'bg-green-900/50 border border-green-500 text-green-200'
            }`}>
              {message}
            </div>
          )}
          {loading && (
            <div className="mt-4 text-blue-400">Processing...</div>
          )}
          {error && (
            <div className="mt-4 p-3 bg-red-900/50 border border-red-500 rounded-md text-red-200">
              Error: {error}
            </div>
          )}
        </div>

        {/* Status Card */}
        <div className="bg-gray-900 rounded-lg p-6 mb-6 border border-gray-800">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className={`w-4 h-4 rounded-full ${getStatusColor(trackingData?.status)}`}></div>
              <span className="text-lg font-medium">Status: {trackingData?.status || 'Not Started'}</span>
            </div>
            <div className="text-sm text-gray-400">
              {(!trackingData?.status || trackingData?.status === 'Not Started') && 'Ready to start your work day'}
              {trackingData?.status === 'On Duty' && 'You are currently working'}
              {trackingData?.status === 'On Break' && 'You are currently on break'}
              {trackingData?.status === 'Completed' && 'Work day completed'}
            </div>
          </div>
        </div>

        {/* Time Tracking Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Time In/Out */}
          <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
            <div className="flex items-center space-x-3 mb-4">
              <Clock className="w-6 h-6 text-blue-400" />
              <h3 className="text-lg font-semibold">Work Time</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Time In:</span>
                <span className="text-sm font-medium">
                  {trackingData?.timeIn || 'Not recorded'}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Time Out:</span>
                <span className="text-sm font-medium">
                  {trackingData?.timeOut || 'Not recorded'}
                </span>
              </div>
              
              <div className="pt-4 space-y-2">
                <button
                  onClick={handleTimeIn}
                  disabled={!canTimeIn}
                  className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
                    canTimeIn
                      ? 'bg-green-600 hover:bg-green-700 border border-green-500'
                      : 'bg-gray-700 border border-gray-600 cursor-not-allowed opacity-50'
                  }`}
                >
                  Time In
                </button>
                
                <button
                  onClick={handleTimeOut}
                  disabled={!canTimeOut}
                  className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
                    canTimeOut
                      ? 'bg-red-600 hover:bg-red-700 border border-red-500'
                      : 'bg-gray-700 border border-gray-600 cursor-not-allowed opacity-50'
                  }`}
                >
                  Time Out
                </button>
              </div>
            </div>
          </div>

          {/* Break In/Out */}
          <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
            <div className="flex items-center space-x-3 mb-4">
              <Coffee className="w-6 h-6 text-yellow-400" />
              <h3 className="text-lg font-semibold">Break Time</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Break In:</span>
                <span className="text-sm font-medium">
                  {trackingData?.breakIn || 'Not recorded'}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Break Out:</span>
                <span className="text-sm font-medium">
                  {trackingData?.breakOut || 'Not recorded'}
                </span>
              </div>
              
              <div className="pt-4 space-y-2">
                <button
                  onClick={handleBreakIn}
                  disabled={!canBreakIn}
                  className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
                    canBreakIn
                      ? 'bg-yellow-600 hover:bg-yellow-700 border border-yellow-500'
                      : 'bg-gray-700 border border-gray-600 cursor-not-allowed opacity-50'
                  }`}
                >
                  Break In
                </button>
                
                <button
                  onClick={handleBreakOut}
                  disabled={!canBreakOut}
                  className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
                    canBreakOut
                      ? 'bg-orange-600 hover:bg-orange-700 border border-orange-500'
                      : 'bg-gray-700 border border-gray-600 cursor-not-allowed opacity-50'
                  }`}
                >
                  Break Out
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Today's Summary */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <h3 className="text-lg font-semibold mb-4">Today's Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-400">
                {trackingData?.timeIn ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Time In</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-yellow-400">
                {trackingData?.breakIn ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Break Taken</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-400">
                {trackingData?.timeOut ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Time Out</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
