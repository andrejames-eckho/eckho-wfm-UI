import React from 'react'
import { getEmployeeStatus, statusColors, formatDate } from '../utils/data'

export default function EmployeeDetails({ employee }) {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">
        Time Records for {employee.firstName} {employee.lastName}
      </h2>

      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-lg font-semibold mb-4">Recent Time Records</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-gray-100">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-3 px-4 text-gray-300">Date</th>
                <th className="py-3 px-4 text-gray-300">Time In</th>
                <th className="py-3 px-4 text-gray-300">Time Out</th>
                <th className="py-3 px-4 text-gray-300">Break</th>
                <th className="py-3 px-4 text-gray-300">Status</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: 7 }, (_, i) => {
                const date = new Date()
                date.setDate(date.getDate() - i)
                return (
                  <tr key={i} className="border-b border-gray-800 hover:bg-gray-800">
                    <td className="py-3 px-4">{formatDate(date)}</td>
                    <td className="py-3 px-4">{employee.timeIn}</td>
                    <td className="py-3 px-4">{employee.timeOut}</td>
                    <td className="py-3 px-4">{employee.breakIn} - {employee.breakOut || 'In Progress'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-3 py-1 rounded-full text-sm text-white ${statusColors[getEmployeeStatus(employee)]}`}>
                        {getEmployeeStatus(employee)}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}


