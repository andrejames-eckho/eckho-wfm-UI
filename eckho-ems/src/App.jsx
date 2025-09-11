import React, { useState, useMemo } from 'react'
import { Helmet } from 'react-helmet-async'
import Header from './components/Header'
import Login from './components/Login'
import DatePicker from './components/DatePicker'
import EmployeeTable from './components/EmployeeTable'
import EmployeeDetails from './components/EmployeeDetails'
import EmployeeRegistration from './components/EmployeeRegistration'
import { 
  dummyEmployees, 
  dummyFieldEmployees, 
  formatDate, 
  getEmployeesWithTimeRecordsForDate,
  adminCredentials
} from './utils/data'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [showUserDropdown, setShowUserDropdown] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [showRegistration, setShowRegistration] = useState(false)

  // Get employees with time records for the selected date
  const fieldEmployeesWithRecords = useMemo(() => {
    return getEmployeesWithTimeRecordsForDate(dummyFieldEmployees, selectedDate)
  }, [selectedDate])

  const warehouseEmployeesWithRecords = useMemo(() => {
    return getEmployeesWithTimeRecordsForDate(dummyEmployees, selectedDate)
  }, [selectedDate])

  const handleLogin = (username, password) => {
    if (username === adminCredentials.username && password === adminCredentials.password) {
      setIsAuthenticated(true)
    } else {
      alert('Invalid username or password')
    }
  }

  const handleDateChange = (date) => {
    setSelectedDate(date)
  }

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee)
  }

  const handleSignOut = () => {
    setIsAuthenticated(false)
    setShowUserDropdown(false)
    setSelectedEmployee(null)
    setShowRegistration(false)
  }

  const handleBackToTable = () => {
    setSelectedEmployee(null)
  }

  const handleShowRegistration = () => {
    setShowRegistration(true)
  }

  const handleBackToDashboard = () => {
    setShowRegistration(false)
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  if (showRegistration) {
    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <Helmet>
          <title>ECKHO EMS - Employee Registration</title>
          <meta name="description" content="Register new employee" />
        </Helmet>
        <Header
          showUserDropdown={showUserDropdown}
          onToggleUserDropdown={() => setShowUserDropdown(!showUserDropdown)}
          onSignOut={handleSignOut}
          rightSlot={(
            <button
              onClick={handleBackToDashboard}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 border border-white rounded-md transition-colors"
            >
              Back to Dashboard
            </button>
          )}
        />
        <EmployeeRegistration />
      </div>
    )
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
        rightSlot={(
          <button
            onClick={handleShowRegistration}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 border border-blue-500 rounded-md transition-colors"
          >
            Register New Employee
          </button>
        )}
      />

      {/* Main Content */}
      <div className="p-6">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-2">Welcome, Admin</h2>
          <p className="text-lg">These are your time stats</p>
        </div>

        <DatePicker selectedDate={selectedDate} onChange={handleDateChange} label={formatDate(selectedDate)} />

        {/* Summary Section */}
        <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-400">
                {fieldEmployeesWithRecords.filter(emp => emp.hasRecordForDate).length}
              </div>
              <div className="text-sm text-gray-400">Field Employees with Records</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-400">
                {warehouseEmployeesWithRecords.filter(emp => emp.hasRecordForDate).length}
              </div>
              <div className="text-sm text-gray-400">Warehouse Employees with Records</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-400">
                {fieldEmployeesWithRecords.filter(emp => emp.hasRecordForDate).length + 
                 warehouseEmployeesWithRecords.filter(emp => emp.hasRecordForDate).length}
              </div>
              <div className="text-sm text-gray-400">Total with Records</div>
            </div>
          </div>
        </div>

        <div className="space-y-10">
          <div>
            <h3 className="text-xl font-semibold mb-4">Field</h3>
            <EmployeeTable employees={fieldEmployeesWithRecords} onRowClick={handleEmployeeClick} />
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-4">Warehouse</h3>
            <EmployeeTable employees={warehouseEmployeesWithRecords} onRowClick={handleEmployeeClick} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
