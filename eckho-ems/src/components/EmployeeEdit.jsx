import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Key } from 'lucide-react'
import { employeeAPI } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import TimePicker from './TimePicker'

const EmployeeEdit = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, userType } = useAuth()
  
  const [employee, setEmployee] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [successMessage, setSuccessMessage] = useState('')
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    type: 'warehouse',
    phoneNumber: '',
    expectedStartTime: '',
    oldPassword: '',
    password: ''
  })

  useEffect(() => {
    if (!isAuthenticated || userType !== 'admin') {
      navigate('/login')
      return
    }
    
    if (id) {
      fetchEmployee()
    }
  }, [id, isAuthenticated, userType, navigate])

  const fetchEmployee = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await employeeAPI.getById(parseInt(id))
      setEmployee(data)
      setFormData({
        firstName: data.firstName || '',
        lastName: data.lastName || '',
        username: data.username || '',
        type: data.type || 'warehouse',
        phoneNumber: data.phoneNumber || '',
        expectedStartTime: data.expectedStartTime || '',
        oldPassword: '', // Don't populate old password for security
        password: '' // Don't populate password for security
      })
    } catch (err) {
      console.error('Error fetching employee:', err)
      setError('Failed to fetch employee details: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Clear messages when user starts typing
    if (error) setError(null)
    if (successMessage) setSuccessMessage('')
  }

  const validateForm = () => {
    const errors = {}
    
    if (!formData.firstName.trim()) {
      errors.firstName = 'First name is required'
    }
    
    if (!formData.lastName.trim()) {
      errors.lastName = 'Last name is required'
    }
    
    if (!formData.username.trim()) {
      errors.username = 'Username is required'
    }
    
    // Expected start time is optional for all employees
    // if (!formData.expectedStartTime) {
    //   errors.expectedStartTime = 'Expected time in is required'
    // }
    
    // If user wants to change password, old password is required
    if (formData.password && !formData.oldPassword) {
      errors.oldPassword = 'Current password is required to set a new password'
    }
    
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const errors = validateForm()
    if (Object.keys(errors).length > 0) {
      setError('Please fix the errors below')
      return
    }

    try {
      setSaving(true)
      setError(null)
      
      const updateData = {
        firstName: formData.firstName.trim(),
        lastName: formData.lastName.trim(),
        username: formData.username.trim(),
        type: formData.type,
        phoneNumber: formData.phoneNumber.trim(),
        expectedStartTime: formData.expectedStartTime || null,
        oldPassword: formData.password ? formData.oldPassword : null, // Send old password only if changing password
        password: formData.password || null // Only send if password is provided
      }

      await employeeAPI.updateEmployee(parseInt(id), updateData)
      setSuccessMessage('Employee details updated successfully!')
      
      // Refresh employee data
      await fetchEmployee()
      
    } catch (err) {
      console.error('Error updating employee:', err)
      setError('Failed to update employee: ' + err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    navigate('/employees')
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <div className="text-gray-400">Loading employee details...</div>
        </div>
      </div>
    )
  }

  if (!employee) {
    return (
      <div className="p-6">
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4">
          <div className="text-red-400 font-semibold mb-2">Employee Not Found</div>
          <div className="text-red-300">The requested employee could not be found.</div>
          <button
            onClick={handleCancel}
            className="mt-3 px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-md transition-colors"
          >
            Back to Employee List
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Edit Employee</h1>
        <p className="text-gray-400">Update employee information and settings</p>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="bg-green-900/20 border border-green-500 rounded-lg p-4 mb-6">
          <div className="text-green-400">{successMessage}</div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-6">
          <div className="text-red-400">{error}</div>
        </div>
      )}

      {/* Employee Info Card */}
      <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Employee ID: #{employee.id}</h3>
            <p className="text-gray-400">Current Status: {employee.status}</p>
          </div>
          <div className="flex items-center">
            <span className="mr-2">{employee.type === 'field' ? '🚛' : '🏭'}</span>
            <span className={`text-sm font-medium capitalize ${
              employee.type === 'field' ? 'text-blue-400' : 'text-green-400'
            }`}>
              {employee.type}
            </span>
          </div>
        </div>
      </div>

      {/* Edit Form */}
      <form onSubmit={handleSubmit} className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* First Name */}
          <div>
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-300 mb-2">
              First Name *
            </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              placeholder="Enter first name"
            />
          </div>

          {/* Last Name */}
          <div>
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-300 mb-2">
              Last Name *
            </label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              placeholder="Enter last name"
            />
          </div>

          {/* Username */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
              Username *
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              placeholder="Enter username"
            />
          </div>

          {/* Employee Type */}
          <div>
            <label htmlFor="type" className="block text-sm font-medium text-gray-300 mb-2">
              Employee Type *
            </label>
            <select
              id="type"
              name="type"
              value={formData.type}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:border-blue-500"
            >
              <option value="warehouse">🏭 Warehouse</option>
              <option value="field">🚛 Field</option>
            </select>
          </div>

          {/* Phone Number */}
          <div>
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-300 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              id="phoneNumber"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleInputChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              placeholder="Enter phone number"
            />
          </div>

          {/* Expected Time In (for all employees) */}
          <div>
            <label htmlFor="expectedStartTime" className="block text-sm font-medium text-gray-300 mb-2">
              Expected Time In
            </label>
            <TimePicker
              value={formData.expectedStartTime}
              onChange={(time) => {
                setFormData(prev => ({
                  ...prev,
                  expectedStartTime: time
                }))
                // Clear messages when user selects a time
                if (error) setError(null)
                if (successMessage) setSuccessMessage('')
              }}
              className="w-full"
            />
            <p className="text-sm text-gray-400 mt-1">Set the expected time for this employee to start work</p>
          </div>

        </div>

        {/* Form Actions */}
        <div className="flex justify-end gap-4 mt-8">
          <button
            type="button"
            onClick={handleCancel}
            className="px-6 py-2 bg-gray-600 hover:bg-gray-700 border border-gray-500 rounded-md transition-colors"
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 border border-blue-500 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Saving...' : 'Save Employee Details'}
          </button>
        </div>
      </form>

      {/* Password Change Section */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 mt-6">
        <div className="mb-6">
          <div className="flex items-center space-x-3 mb-2">
            <Key className="w-5 h-5 text-orange-400" />
            <h3 className="text-lg font-semibold text-gray-200">Change Password</h3>
          </div>
          <p className="text-gray-400 text-sm">Update the employee's login password. Both fields are required to change the password.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Current Password */}
            <div>
              <label htmlFor="oldPassword" className="block text-sm font-medium text-gray-300 mb-2">
                Current Password *
              </label>
              <input
                type="password"
                id="oldPassword"
                name="oldPassword"
                value={formData.oldPassword}
                onChange={handleInputChange}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                placeholder="Enter current password"
              />
              <p className="text-sm text-gray-400 mt-1">Required to verify identity</p>
            </div>

            {/* New Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                New Password *
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                placeholder="Enter new password"
              />
              <p className="text-sm text-gray-400 mt-1">Minimum 6 characters</p>
            </div>
          </div>

          {/* Password Change Actions */}
          <div className="flex justify-end gap-4 pt-4 border-t border-gray-700">
            <button
              type="button"
              onClick={() => {
                setFormData(prev => ({
                  ...prev,
                  oldPassword: '',
                  password: ''
                }))
                if (error) setError(null)
                if (successMessage) setSuccessMessage('')
              }}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 border border-gray-500 rounded-md transition-colors text-sm"
              disabled={saving}
            >
              Clear
            </button>
            <button
              type="submit"
              disabled={saving || !formData.oldPassword || !formData.password}
              className="px-6 py-2 bg-orange-600 hover:bg-orange-700 border border-orange-500 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            >
              {saving ? 'Updating Password...' : 'Update Password'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EmployeeEdit
