import React from 'react'
import { Calendar } from 'lucide-react'

export default function DatePicker({ selectedDate, onChange, label }) {
  return (
    <div className="mb-6 flex justify-center">
      <div className="flex items-center space-x-3">
        <Calendar className="w-5 h-5" />
        <input
          type="date"
          value={selectedDate.toISOString().split('T')[0]}
          onChange={(e) => onChange(new Date(e.target.value))}
          className="bg-gray-700 text-white px-4 py-2 rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {label && (
          <span className="text-lg font-medium">{label}</span>
        )}
      </div>
    </div>
  )
}


