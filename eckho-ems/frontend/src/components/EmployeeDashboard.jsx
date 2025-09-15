import React, { useState, useEffect } from 'react'
import { Clock, Coffee, LogOut, User } from 'lucide-react'
import { employeeTimeTracking, getEmployeeStatus } from '../utils/data'

export default function EmployeeDashboard({ employee, onSignOut }) {
  const [timeTracking, setTimeTracking] = useState(null)
  const [currentTime, setCurrentTime] = useState(new Date())

  // Update current time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  // Initialize time tracking for the employee
  useEffect(() => {
    const tracking = employeeTimeTracking.getTracking(employee.id)
    setTimeTracking(tracking)
  }, [employee.id])

  const handleTimeIn = () => {
    const updatedTracking = employeeTimeTracking.timeIn(employee.id)
    setTimeTracking({ ...updatedTracking })
  }

  const handleTimeOut = () => {
    const updatedTracking = employeeTimeTracking.timeOut(employee.id)
    setTimeTracking({ ...updatedTracking })
  }

  const handleBreakIn = () => {
    const updatedTracking = employeeTimeTracking.breakIn(employee.id)
    setTimeTracking({ ...updatedTracking })
  }

  const handleBreakOut = () => {
    const updatedTracking = employeeTimeTracking.breakOut(employee.id)
    setTimeTracking({ ...updatedTracking })
  }

  const getStatusColor = (status) => {
    const colors = {
      'Not Started': 'bg-gray-600',
      'On Duty': 'bg-green-500',
      'On Break': 'bg-yellow-500',
      'Completed': 'bg-blue-500'
    }
    return colors[status] || 'bg-gray-600'
  }

  const canTimeIn = !timeTracking?.timeIn
  const canTimeOut = timeTracking?.timeIn && !timeTracking?.timeOut && timeTracking?.status !== 'On Break'
  const canBreakIn = timeTracking?.timeIn && !timeTracking?.timeOut && !timeTracking?.breakIn
  const canBreakOut = timeTracking?.breakIn && !timeTracking?.breakOut

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
            Welcome, {employee.firstName}!
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
        </div>

        {/* Status Card */}
        <div className="bg-gray-900 rounded-lg p-6 mb-6 border border-gray-800">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className={`w-4 h-4 rounded-full ${getStatusColor(timeTracking?.status)}`}></div>
              <span className="text-lg font-medium">Status: {timeTracking?.status}</span>
            </div>
            <div className="text-sm text-gray-400">
              {timeTracking?.status === 'Not Started' && 'Ready to start your work day'}
              {timeTracking?.status === 'On Duty' && 'You are currently working'}
              {timeTracking?.status === 'On Break' && 'You are currently on break'}
              {timeTracking?.status === 'Completed' && 'Work day completed'}
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
                  {timeTracking?.timeIn || 'Not recorded'}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Time Out:</span>
                <span className="text-sm font-medium">
                  {timeTracking?.timeOut || 'Not recorded'}
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
                  {timeTracking?.breakIn || 'Not recorded'}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Break Out:</span>
                <span className="text-sm font-medium">
                  {timeTracking?.breakOut || 'Not recorded'}
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
                {timeTracking?.timeIn ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Time In</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-yellow-400">
                {timeTracking?.breakIn ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Break Taken</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-400">
                {timeTracking?.timeOut ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-400">Time Out</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
