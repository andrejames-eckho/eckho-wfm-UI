import React, { useState, useMemo, useEffect } from 'react'
import { Helmet } from 'react-helmet-async'
import { Routes, Route, useNavigate, useLocation, useParams } from 'react-router-dom'
import Header from './components/Header'
import Login from './components/Login'
import EmployeeDashboard from './components/EmployeeDashboard'
import DatePicker from './components/DatePicker'
import EmployeeTable from './components/EmployeeTable'
import EmployeeDetails from './components/EmployeeDetails'
import EmployeeRegistration from './components/EmployeeRegistration'
import { 
  dummyEmployees, 
  dummyFieldEmployees, 
  formatDate, 
  getEmployeesWithTimeRecordsForDate,
  adminCredentials,
  employeeCredentials
} from './utils/data'

function App() {
  const navigate = useNavigate()
  const location = useLocation()
  
  // Initialize authentication state from localStorage
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('eckho_authenticated') === 'true'
  })
  
  const [userType, setUserType] = useState(() => {
    return localStorage.getItem('eckho_user_type') || 'admin' // 'admin' or 'employee'
  })
  
  const [currentEmployee, setCurrentEmployee] = useState(() => {
    const savedEmployee = localStorage.getItem('eckho_current_employee')
    return savedEmployee ? JSON.parse(savedEmployee) : null
  })
  
  const [selectedDate, setSelectedDate] = useState(() => {
    const savedDate = localStorage.getItem('eckho_selected_date')
    return savedDate ? new Date(savedDate) : new Date()
  })
  
  const [showUserDropdown, setShowUserDropdown] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [showRegistration, setShowRegistration] = useState(false)

  // Save authentication state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('eckho_authenticated', isAuthenticated.toString())
  }, [isAuthenticated])

  // Save user type to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('eckho_user_type', userType)
  }, [userType])

  // Save current employee to localStorage whenever it changes
  useEffect(() => {
    if (currentEmployee) {
      localStorage.setItem('eckho_current_employee', JSON.stringify(currentEmployee))
    } else {
      localStorage.removeItem('eckho_current_employee')
    }
  }, [currentEmployee])

  // Save selected date to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('eckho_selected_date', selectedDate.toISOString())
  }, [selectedDate])

  // Handle authentication state changes
  useEffect(() => {
    if (!isAuthenticated) {
      if (location.pathname !== '/login') {
        navigate('/login')
      }
    } else if (isAuthenticated) {
      if (location.pathname === '/login') {
        // Redirect based on user type
        if (userType === 'employee') {
          navigate('/employee-dashboard')
        } else {
          navigate('/')
        }
      }
    }
  }, [isAuthenticated, userType, location.pathname, navigate])

  // Get employees with time records for the selected date
  const fieldEmployeesWithRecords = useMemo(() => {
    return getEmployeesWithTimeRecordsForDate(dummyFieldEmployees, selectedDate)
  }, [selectedDate])

  const warehouseEmployeesWithRecords = useMemo(() => {
    return getEmployeesWithTimeRecordsForDate(dummyEmployees, selectedDate)
  }, [selectedDate])

  const handleLogin = (username, password, userType, employeeId = null) => {
    if (userType === 'admin') {
      setIsAuthenticated(true)
      setUserType('admin')
      setCurrentEmployee(null)
      navigate('/')
    } else if (userType === 'employee' && employeeId) {
      // Find the employee data
      const allEmployees = [...dummyEmployees, ...dummyFieldEmployees]
      const employee = allEmployees.find(emp => emp.id === employeeId)
      
      if (employee) {
        setIsAuthenticated(true)
        setUserType('employee')
        setCurrentEmployee(employee)
        navigate('/employee-dashboard')
      } else {
        alert('Employee data not found')
      }
    } else {
      alert('Invalid credentials')
    }
  }

  const handleDateChange = (date) => {
    setSelectedDate(date)
  }


  const handleSignOut = () => {
    setIsAuthenticated(false)
    setUserType('admin')
    setCurrentEmployee(null)
    setShowUserDropdown(false)
    setSelectedEmployee(null)
    setShowRegistration(false)
    localStorage.removeItem('eckho_authenticated')
    localStorage.removeItem('eckho_user_type')
    localStorage.removeItem('eckho_current_employee')
    localStorage.removeItem('eckho_selected_date')
    navigate('/login')
  }


  const handleBackToTable = () => {
    setSelectedEmployee(null)
    navigate('/')
  }

  const handleShowRegistration = () => {
    navigate('/register')
  }

  const handleBackToDashboard = () => {
    navigate('/')
  }

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee)
    navigate(`/employee/${employee.id}`)
  }

  // Component for Dashboard
  const Dashboard = () => {
    // Access control - only admin can access dashboard
    if (userType !== 'admin') {
      navigate('/employee-dashboard')
      return null
    }

    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <Helmet>
          <title>ECKHO WFM - Dashboard</title>
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

  // Component for Employee Details
  const EmployeeDetailsPage = () => {
    // Access control - only admin can access employee details
    if (userType !== 'admin') {
      navigate('/employee-dashboard')
      return null
    }

    const { id } = useParams()
    const employeeId = parseInt(id, 10)
    const allEmployees = [...dummyFieldEmployees, ...dummyEmployees]
    const employee = allEmployees.find(emp => emp.id === employeeId)
    
    if (!employee || isNaN(employeeId)) {
      navigate('/')
      return null
    }

    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <Helmet>
          <title>{`ECKHO WFM - ${employee.firstName} ${employee.lastName}`}</title>
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
        <EmployeeDetails employee={employee} />
      </div>
    )
  }

  // Component for Registration
  const RegistrationPage = () => {
    // Access control - only admin can access registration
    if (userType !== 'admin') {
      navigate('/employee-dashboard')
      return null
    }

    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <Helmet>
          <title>ECKHO WFM - Employee Registration</title>
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

  // Component for Employee Dashboard
  const EmployeeDashboardPage = () => {
    if (!currentEmployee) {
      navigate('/employee-login')
      return null
    }

    return (
      <EmployeeDashboard 
        employee={currentEmployee} 
        onSignOut={handleSignOut}
      />
    )
  }

  return (
    <Routes>
      <Route path="/login" element={<Login onLogin={handleLogin} />} />
      <Route path="/employee-dashboard" element={<EmployeeDashboardPage />} />
      <Route path="/" element={<Dashboard />} />
      <Route path="/register" element={<RegistrationPage />} />
      <Route path="/employee/:id" element={<EmployeeDetailsPage />} />
      <Route path="*" element={<Dashboard />} />
    </Routes>
  )
}

export default App
