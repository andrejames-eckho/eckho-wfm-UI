import React, { useState } from 'react'
import { Target, User, Calendar, LogOut } from 'lucide-react'

// Dummy employee data
const dummyEmployees = [
  {
    id: 1,
    firstName: 'John',
    lastName: 'Smith',
    timeIn: '08:00 AM',
    timeOut: '05:00 PM',
    breakIn: '12:00 PM',
    breakOut: '01:00 PM',
    status: 'On Duty'
  },
  {
    id: 2,
    firstName: 'Sarah',
    lastName: 'Johnson',
    timeIn: '08:15 AM',
    timeOut: '06:30 PM',
    breakIn: '12:30 PM',
    breakOut: '01:30 PM',
    status: 'Overtime'
  },
  {
    id: 3,
    firstName: 'Mike',
    lastName: 'Davis',
    timeIn: '09:30 AM',
    timeOut: '05:00 PM',
    breakIn: '12:00 PM',
    breakOut: '01:00 PM',
    status: 'Late'
  },
  {
    id: 4,
    firstName: 'Emily',
    lastName: 'Wilson',
    timeIn: '08:00 AM',
    timeOut: '04:30 PM',
    breakIn: '02:00 PM',
    breakOut: null, // Currently on break
    status: 'On Break'
  },
  {
    id: 5,
    firstName: 'David',
    lastName: 'Brown',
    timeIn: '08:00 AM',
    timeOut: '04:00 PM',
    breakIn: '12:00 PM',
    breakOut: '01:00 PM',
    status: 'Undertime'
  },
  {
    id: 6,
    firstName: 'Lisa',
    lastName: 'Anderson',
    timeIn: '08:00 AM',
    timeOut: '05:00 PM',
    breakIn: '03:30 PM',
    breakOut: null, // Currently on break
    status: 'On Duty'
  }
]

const statusColors = {
  'On Duty': 'bg-green-500',
  'On Break': 'bg-gray-500',
  'Overtime': 'bg-blue-500',
  'Late': 'bg-red-500',
  'Undertime': 'bg-yellow-500'
}

// Function to determine employee status based on break times
const getEmployeeStatus = (employee) => {
  // If employee has breakIn time but no breakOut time, they are currently on break
  if (employee.breakIn && !employee.breakOut) {
    return 'On Break'
  }
  // Otherwise, use the predefined status
  return employee.status
}

function App() {
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [showUserDropdown, setShowUserDropdown] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const handleDateChange = (event) => {
    setSelectedDate(new Date(event.target.value))
  }

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee)
  }

  const handleSignOut = () => {
    alert('Sign out functionality would be implemented here')
    setShowUserDropdown(false)
  }

  const handleBackToTable = () => {
    setSelectedEmployee(null)
  }

  if (selectedEmployee) {
    return (
      <div className="min-h-screen bg-eckho-dark text-white">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white">
          <div className="flex items-center space-x-3">
            <Target className="w-8 h-8 text-white" />
            <h1 className="text-xl font-semibold">ECKHO Workforce Management</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={handleBackToTable}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
            >
              Back to Table
            </button>
            <div className="relative">
              <button
                onClick={() => setShowUserDropdown(!showUserDropdown)}
                className="p-2 hover:bg-gray-700 rounded-full transition-colors"
              >
                <User className="w-6 h-6" />
              </button>
              {showUserDropdown && (
                <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-md shadow-lg z-10">
                  <button
                    onClick={handleSignOut}
                    className="flex items-center w-full px-4 py-2 text-left hover:bg-gray-700 transition-colors"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Employee Details */}
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-6">
            Time Records for {selectedEmployee.firstName} {selectedEmployee.lastName}
          </h2>
          
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Recent Time Records</h3>
            <div className="space-y-4">
              {Array.from({ length: 7 }, (_, i) => {
                const date = new Date()
                date.setDate(date.getDate() - i)
                return (
                  <div key={i} className="flex justify-between items-center p-4 bg-gray-700 rounded-md">
                    <div>
                      <span className="font-medium">{formatDate(date)}</span>
                    </div>
                    <div className="flex space-x-6">
                      <span>In: {selectedEmployee.timeIn}</span>
                      <span>Out: {selectedEmployee.timeOut}</span>
                      <span>Break: {selectedEmployee.breakIn} - {selectedEmployee.breakOut || 'In Progress'}</span>
                      <span className={`px-3 py-1 rounded-full text-sm text-white ${statusColors[getEmployeeStatus(selectedEmployee)]}`}>
                        {getEmployeeStatus(selectedEmployee)}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-eckho-dark text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-white">
        <div className="flex items-center space-x-3">
          <Target className="w-8 h-8 text-white" />
          <h1 className="text-xl font-semibold">ECKHO Workforce Management</h1>
        </div>
        <div className="relative">
          <button
            onClick={() => setShowUserDropdown(!showUserDropdown)}
            className="p-2 hover:bg-gray-700 rounded-full transition-colors"
          >
            <User className="w-6 h-6" />
          </button>
          {showUserDropdown && (
            <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-md shadow-lg z-10">
              <button
                onClick={handleSignOut}
                className="flex items-center w-full px-4 py-2 text-left hover:bg-gray-700 transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-2">Welcome, Admin</h2>
          <p className="text-lg">These are your time stats</p>
        </div>

        {/* Date Picker */}
        <div className="mb-6 flex justify-center">
          <div className="flex items-center space-x-3">
            <Calendar className="w-5 h-5" />
            <input
              type="date"
              value={selectedDate.toISOString().split('T')[0]}
              onChange={handleDateChange}
              className="bg-gray-700 text-white px-4 py-2 rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <span className="text-lg font-medium">{formatDate(selectedDate)}</span>
          </div>
        </div>

        {/* Employee Table */}
        <div className="bg-eckho-light rounded-lg p-6">
          <div className="overflow-x-auto">
            <table className="w-full text-gray-800">
              <thead>
                <tr className="border-b-2 border-gray-400">
                  <th className="text-left py-3 px-4 font-semibold">First Name</th>
                  <th className="text-left py-3 px-4 font-semibold">Last Name</th>
                  <th className="text-left py-3 px-4 font-semibold">Time In</th>
                  <th className="text-left py-3 px-4 font-semibold">Time Out</th>
                  <th className="text-left py-3 px-4 font-semibold">Break In</th>
                  <th className="text-left py-3 px-4 font-semibold">Break Out</th>
                  <th className="text-left py-3 px-4 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                {dummyEmployees.map((employee) => (
                  <tr
                    key={employee.id}
                    onClick={() => handleEmployeeClick(employee)}
                    className="border-b border-gray-300 hover:bg-gray-200 cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-4">{employee.firstName}</td>
                    <td className="py-3 px-4">{employee.lastName}</td>
                    <td className="py-3 px-4">{employee.timeIn}</td>
                    <td className="py-3 px-4">{employee.timeOut}</td>
                    <td className="py-3 px-4">{employee.breakIn}</td>
                    <td className="py-3 px-4">{employee.breakOut || 'In Progress'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-3 py-1 rounded-full text-sm text-white ${statusColors[getEmployeeStatus(employee)]}`}>
                        {getEmployeeStatus(employee)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
