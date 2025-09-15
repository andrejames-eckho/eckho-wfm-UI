import React, { useState } from 'react'
import { Calendar, X } from 'lucide-react'

export default function DateRangePicker({ onDateRangeChange, isOpen, onToggle }) {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const handleApply = () => {
    if (startDate && endDate) {
      onDateRangeChange(new Date(startDate), new Date(endDate))
      onToggle()
    }
  }

  const handleClear = () => {
    setStartDate('')
    setEndDate('')
    onDateRangeChange(null, null)
    onToggle()
  }

  const handleClose = () => {
    onToggle()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 w-96 border border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Select Date Range</h3>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Start Date
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full pl-10 pr-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              End Date
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full pl-10 pr-3 py-2 bg-gray-700 text-white rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <div className="flex space-x-3 mt-6">
          <button
            onClick={handleApply}
            disabled={!startDate || !endDate}
            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-md transition-colors"
          >
            Apply
          </button>
          <button
            onClick={handleClear}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  )
}
