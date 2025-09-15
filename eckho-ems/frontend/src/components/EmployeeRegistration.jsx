import React, { useState } from 'react'
import { UserPlus, Camera, Fingerprint, Upload, CheckCircle } from 'lucide-react'

export default function EmployeeRegistration() {
  const [formData, setFormData] = useState({
    idNumber: '',
    firstName: '',
    lastName: '',
    department: ''
  })

  const [errors, setErrors] = useState({})
  const [biometricData, setBiometricData] = useState({
    faceData: null,
    fingerprintData: null,
    faceCaptured: false,
    fingerprintCaptured: false
  })

  const departments = [
    'Field Operations',
    'Warehouse',
    'Administration',
    'Management',
    'IT Support',
    'Human Resources'
  ]

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.idNumber.trim()) {
      newErrors.idNumber = 'ID Number is required'
    } else if (!/^\d+$/.test(formData.idNumber.trim())) {
      newErrors.idNumber = 'ID Number must contain only numbers'
    }
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First Name is required'
    }
    
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last Name is required'
    }
    
    if (!formData.department) {
      newErrors.department = 'Department is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleFaceCapture = () => {
    // Simulate face capture process
    setTimeout(() => {
      setBiometricData(prev => ({
        ...prev,
        faceData: 'face_template_data_12345',
        faceCaptured: true
      }))
    }, 1500)
  }

  const handleFingerprintCapture = () => {
    // Simulate fingerprint capture process
    setTimeout(() => {
      setBiometricData(prev => ({
        ...prev,
        fingerprintData: 'fingerprint_template_data_67890',
        fingerprintCaptured: true
      }))
    }, 2000)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (validateForm()) {
      // For now, just show success message
      alert(`Employee ${formData.firstName} ${formData.lastName} registered successfully!`)
      
      // Reset form
      setFormData({
        idNumber: '',
        firstName: '',
        lastName: '',
        department: ''
      })
      
      // Reset biometric data
      setBiometricData({
        faceData: null,
        fingerprintData: null,
        faceCaptured: false,
        fingerprintCaptured: false
      })
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="p-6">
        {/* Header Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <UserPlus className="w-8 h-8 text-white-400" />
            <h1 className="text-2xl font-semibold">Employee Registration</h1>
          </div>
        </div>

        {/* Registration Form */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-gray-900 rounded-lg p-8 border border-gray-800">
            <div className="text-center mb-8">
              <h2 className="text-xl font-semibold mb-2">Register New Employee</h2>
              <p className="text-gray-400">Enter the employee information below</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* ID Number */}
              <div>
                <label htmlFor="idNumber" className="block text-sm font-medium text-gray-300 mb-2">
                  ID Number *
                </label>
                <input
                  type="text"
                  id="idNumber"
                  name="idNumber"
                  value={formData.idNumber}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-3 bg-gray-800 border rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                    errors.idNumber ? 'border-red-500' : 'border-gray-600'
                  }`}
                  placeholder="Enter employee ID number"
                />
                {errors.idNumber && (
                  <p className="mt-1 text-sm text-red-400">{errors.idNumber}</p>
                )}
              </div>

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
                  className={`w-full px-4 py-3 bg-gray-800 border rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                    errors.firstName ? 'border-red-500' : 'border-gray-600'
                  }`}
                  placeholder="Enter first name"
                />
                {errors.firstName && (
                  <p className="mt-1 text-sm text-red-400">{errors.firstName}</p>
                )}
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
                  className={`w-full px-4 py-3 bg-gray-800 border rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                    errors.lastName ? 'border-red-500' : 'border-gray-600'
                  }`}
                  placeholder="Enter last name"
                />
                {errors.lastName && (
                  <p className="mt-1 text-sm text-red-400">{errors.lastName}</p>
                )}
              </div>

              {/* Department */}
              <div>
                <label htmlFor="department" className="block text-sm font-medium text-gray-300 mb-2">
                  Department *
                </label>
                <select
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-3 bg-gray-800 border rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                    errors.department ? 'border-red-500' : 'border-gray-600'
                  }`}
                >
                  <option value="">Select a department</option>
                  {departments.map((dept) => (
                    <option key={dept} value={dept} className="bg-gray-800">
                      {dept}
                    </option>
                  ))}
                </select>
                {errors.department && (
                  <p className="mt-1 text-sm text-red-400">{errors.department}</p>
                )}
              </div>

              {/* Biometric Data Section */}
              <div className="border-t border-gray-700 pt-6">
                <h3 className="text-lg font-semibold text-gray-200 mb-4">Biometric Data</h3>
                
                {/* Face Recognition */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Face Recognition Data
                  </label>
                  <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Camera className="w-6 h-6 text-blue-400" />
                        <div>
                          <p className="text-sm text-gray-300">
                            {biometricData.faceCaptured ? 'Face data captured successfully' : 'Capture face data from external device'}
                          </p>
                          {biometricData.faceCaptured && (
                            <p className="text-xs text-green-400 mt-1">Template ID: {biometricData.faceData}</p>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {biometricData.faceCaptured ? (
                          <div className="flex items-center space-x-2 text-green-400">
                            <CheckCircle className="w-5 h-5" />
                            <span className="text-sm">Captured</span>
                          </div>
                        ) : (
                          <button
                            type="button"
                            onClick={handleFaceCapture}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-md transition-colors flex items-center space-x-2"
                          >
                            <Camera className="w-4 h-4" />
                            <span>Capture Face</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Fingerprint Recognition */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Fingerprint Data
                  </label>
                  <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Fingerprint className="w-6 h-6 text-green-400" />
                        <div>
                          <p className="text-sm text-gray-300">
                            {biometricData.fingerprintCaptured ? 'Fingerprint data captured successfully' : 'Capture fingerprint data from external device'}
                          </p>
                          {biometricData.fingerprintCaptured && (
                            <p className="text-xs text-green-400 mt-1">Template ID: {biometricData.fingerprintData}</p>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {biometricData.fingerprintCaptured ? (
                          <div className="flex items-center space-x-2 text-green-400">
                            <CheckCircle className="w-5 h-5" />
                            <span className="text-sm">Captured</span>
                          </div>
                        ) : (
                          <button
                            type="button"
                            onClick={handleFingerprintCapture}
                            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-md transition-colors flex items-center space-x-2"
                          >
                            <Fingerprint className="w-4 h-4" />
                            <span>Capture Fingerprint</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* External Device Status */}
                <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
                  <div className="flex items-center space-x-3">
                    <Upload className="w-5 h-5 text-yellow-400" />
                    <div>
                      <p className="text-sm text-gray-300">External Device Status</p>
                      <p className="text-xs text-yellow-400 mt-1">Ready to receive biometric data</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
                >
                  Register Employee
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
