import React from 'react'
import { getEmployeeStatus, statusColors } from '../utils/data'

export default function EmployeeTable({ employees, onRowClick }) {
  const showExpectedColumn = employees.some((e) => !!e.expectedStartTime)
  
  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-gray-100">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-3 px-4 text-gray-300">First Name</th>
              <th className="py-3 px-4 text-gray-300">Last Name</th>
              {showExpectedColumn && (
                <th className="py-3 px-4 text-gray-300">Expected Time In</th>
              )}
              <th className="py-3 px-4 text-gray-300">Time In</th>
              <th className="py-3 px-4 text-gray-300">Time Out</th>
              <th className="py-3 px-4 text-gray-300">Break In</th>
              <th className="py-3 px-4 text-gray-300">Break Out</th>
              <th className="py-3 px-4 text-gray-300">Status</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => {
              const hasRecord = employee.hasRecordForDate
              const status = employee.status || getEmployeeStatus(employee)
              
              return (
                <tr
                  key={employee.id}
                  onClick={() => onRowClick(employee)}
                  className={`border-b border-gray-800 hover:bg-gray-800 cursor-pointer transition-colors ${
                    !hasRecord ? 'opacity-60' : ''
                  }`}
                >
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <span>{employee.firstName}</span>
                      {!hasRecord && (
                        <span className="text-xs text-gray-500">(No record)</span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4">{employee.lastName}</td>
                  {showExpectedColumn && (
                    <td className="py-3 px-4">{employee.expectedStartTime || '-'}</td>
                  )}
                  <td className={`py-3 px-4 ${!hasRecord ? 'text-gray-500' : ''}`}>
                    {employee.timeIn}
                  </td>
                  <td className={`py-3 px-4 ${!hasRecord ? 'text-gray-500' : ''}`}>
                    {employee.timeOut}
                  </td>
                  <td className={`py-3 px-4 ${!hasRecord ? 'text-gray-500' : ''}`}>
                    {employee.breakIn}
                  </td>
                  <td className={`py-3 px-4 ${!hasRecord ? 'text-gray-500' : ''}`}>
                    {employee.breakOut}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm text-white ${statusColors[status]}`}>
                      {status}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}


