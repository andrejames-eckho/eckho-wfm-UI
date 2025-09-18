import React, { useState, useEffect, useRef } from 'react'
import { Clock } from 'lucide-react'

const TimePicker = ({ value, onChange, className = '', error = false }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedHour, setSelectedHour] = useState('09')
  const [selectedMinute, setSelectedMinute] = useState('00')
  const [selectedPeriod, setSelectedPeriod] = useState('AM')
  const dropdownRef = useRef(null)

  // Generate hours (1-12)
  const hours = Array.from({ length: 12 }, (_, i) => {
    const hour = i + 1
    return hour.toString().padStart(2, '0')
  })

  // Generate minutes (00, 15, 30, 45)
  const minutes = ['00', '15', '30', '45']

  // Parse the current value when component mounts or value changes
  useEffect(() => {
    if (value) {
      // Handle both HH:MM and HH:MM AM/PM formats
      const timeMatch = value.match(/^(\d{1,2}):(\d{2})(?:\s*(AM|PM))?$/i)
      if (timeMatch) {
        let hour = parseInt(timeMatch[1])
        const minute = timeMatch[2]
        let period = timeMatch[3] || (hour >= 12 ? 'PM' : 'AM')

        // Convert 24-hour to 12-hour format if needed
        if (hour === 0) {
          hour = 12
          period = 'AM'
        } else if (hour > 12) {
          hour = hour - 12
          period = 'PM'
        } else if (hour === 12) {
          period = 'PM'
        }

        setSelectedHour(hour.toString().padStart(2, '0'))
        setSelectedMinute(minute)
        setSelectedPeriod(period.toUpperCase())
      }
    }
  }, [value])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleTimeChange = (hour, minute, period) => {
    setSelectedHour(hour)
    setSelectedMinute(minute)
    setSelectedPeriod(period)
    
    // Format the time and call onChange
    const formattedTime = `${hour}:${minute} ${period}`
    onChange(formattedTime)
  }

  const displayValue = value || 'Select time'

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Time Input Display */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full px-4 py-3 bg-gray-800 border rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors cursor-pointer flex items-center justify-between ${
          error ? 'border-red-500' : 'border-gray-600'
        } ${className}`}
      >
        <span className={value ? 'text-white' : 'text-gray-400'}>
          {displayValue}
        </span>
        <Clock className="w-5 h-5 text-gray-400" />
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-600 rounded-md shadow-lg z-50">
          <div className="p-4">
            <div className="grid grid-cols-3 gap-4">
              {/* Hours */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Hour</label>
                <div className="max-h-32 overflow-y-auto border border-gray-600 rounded">
                  {hours.map((hour) => (
                    <div
                      key={hour}
                      onClick={() => handleTimeChange(hour, selectedMinute, selectedPeriod)}
                      className={`px-3 py-2 cursor-pointer hover:bg-gray-700 transition-colors ${
                        selectedHour === hour ? 'bg-blue-600 text-white' : 'text-gray-300'
                      }`}
                    >
                      {hour}
                    </div>
                  ))}
                </div>
              </div>

              {/* Minutes */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Minute</label>
                <div className="max-h-32 overflow-y-auto border border-gray-600 rounded">
                  {minutes.map((minute) => (
                    <div
                      key={minute}
                      onClick={() => handleTimeChange(selectedHour, minute, selectedPeriod)}
                      className={`px-3 py-2 cursor-pointer hover:bg-gray-700 transition-colors ${
                        selectedMinute === minute ? 'bg-blue-600 text-white' : 'text-gray-300'
                      }`}
                    >
                      {minute}
                    </div>
                  ))}
                </div>
              </div>

              {/* AM/PM */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Period</label>
                <div className="border border-gray-600 rounded">
                  {['AM', 'PM'].map((period) => (
                    <div
                      key={period}
                      onClick={() => handleTimeChange(selectedHour, selectedMinute, period)}
                      className={`px-3 py-2 cursor-pointer hover:bg-gray-700 transition-colors ${
                        selectedPeriod === period ? 'bg-blue-600 text-white' : 'text-gray-300'
                      }`}
                    >
                      {period}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-2 mt-4 pt-4 border-t border-gray-600">
              <button
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 text-sm bg-gray-600 hover:bg-gray-700 text-white rounded transition-colors"
              >
                Done
              </button>
              <button
                onClick={() => {
                  setSelectedHour('09')
                  setSelectedMinute('00')
                  setSelectedPeriod('AM')
                  onChange('')
                }}
                className="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
              >
                Clear
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TimePicker
