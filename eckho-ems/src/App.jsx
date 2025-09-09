import React, { useState } from 'react'
import { Helmet } from 'react-helmet-async'
import Header from './components/Header'
import DatePicker from './components/DatePicker'
import EmployeeTable from './components/EmployeeTable'
import EmployeeDetails from './components/EmployeeDetails'
import { dummyEmployees, dummyFieldEmployees, formatDate } from './utils/data'

function App() {
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [showUserDropdown, setShowUserDropdown] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  const handleDateChange = (date) => {
    setSelectedDate(date)
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
      <div className="min-h-screen bg-gray-950 text-white">
        <Helmet>
          <title>{`ECKHO EMS - ${selectedEmployee.firstName} ${selectedEmployee.lastName}`}</title>
          <meta name="description" content="Employee time records details" />
        </Helmet>
        <Header
          showUserDropdown={showUserDropdown}
          onToggleUserDropdown={() => setShowUserDropdown(!showUserDropdown)}
          onSignOut={handleSignOut}
          rightSlot={(
            <button
              onClick={handleBackToTable}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 border border-white rounded-md transition-colors"
            >
              Back to Table
            </button>
          )}
        />
        <EmployeeDetails employee={selectedEmployee} />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Helmet>
        <title>ECKHO EMS - Dashboard</title>
        <meta name="description" content="Employee management dashboard" />
      </Helmet>
      <Header
        showUserDropdown={showUserDropdown}
        onToggleUserDropdown={() => setShowUserDropdown(!showUserDropdown)}
        onSignOut={handleSignOut}
      />

      {/* Main Content */}
      <div className="p-6">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-2">Welcome, Admin</h2>
          <p className="text-lg">These are your time stats</p>
        </div>

        <DatePicker selectedDate={selectedDate} onChange={handleDateChange} label={formatDate(selectedDate)} />

        <div className="space-y-10">
          <div>
            <h3 className="text-xl font-semibold mb-4">Field</h3>
            <EmployeeTable employees={dummyFieldEmployees} onRowClick={handleEmployeeClick} />
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-4">Warehouse</h3>
            <EmployeeTable employees={dummyEmployees} onRowClick={handleEmployeeClick} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
