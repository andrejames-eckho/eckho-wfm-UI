import React, { useState, useEffect, useMemo } from 'react'
import { employeeAPI } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

const EmployeeManagement = () => {
  const { isAuthenticated, userType } = useAuth()
  const navigate = useNavigate()
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all') // all, field, warehouse
  const [sortBy, setSortBy] = useState('name') // name, id, type, status
  const [sortDirection, setSortDirection] = useState('asc') // asc, desc
  const [activeFilters, setActiveFilters] = useState({
    id: false,
    name: false,
    type: false,
    status: false
  })

  useEffect(() => {
    if (isAuthenticated && userType === 'admin') {
      fetchEmployees()
    } else {
      setLoading(false)
      setError('Access denied. Admin authentication required.')
    }
  }, [isAuthenticated, userType])

  const fetchEmployees = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await employeeAPI.getAll()
      console.log('Fetched employees:', data)
      
      // Handle the nested response format from the API
      const employeeList = data.employees || data || []
      setEmployees(Array.isArray(employeeList) ? employeeList : [])
    } catch (err) {
      console.error('Error fetching employees:', err)
      setError('Failed to fetch employees: ' + err.message)
      setEmployees([])
    } finally {
      setLoading(false)
    }
  }

  const handleFilterToggle = (filterType) => {
    // If clicking the same column, toggle direction
    if (sortBy === filterType) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc')
    } else {
      // If clicking a different column, set new sort and default to ascending
      setSortBy(filterType)
      setSortDirection('asc')
    }
    
    setActiveFilters(prev => ({
      ...prev,
      [filterType]: !prev[filterType]
    }))
  }

  // Filter and sort employees
  const filteredAndSortedEmployees = useMemo(() => {
    if (!Array.isArray(employees) || employees.length === 0) {
      return []
    }

    let filtered = employees.filter(employee => {
      // Safe access to employee properties
      const firstName = employee.firstName || ''
      const lastName = employee.lastName || ''
      const username = employee.username || ''
      const id = employee.id ? employee.id.toString() : ''
      const type = employee.type || ''

      const matchesSearch = 
        firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        id.includes(searchTerm)

      const matchesFilter = 
        filterType === 'all' ||
        (filterType === 'field' && type === 'field') ||
        (filterType === 'warehouse' && type === 'warehouse')

      return matchesSearch && matchesFilter
    })

    // Sort employees
    filtered.sort((a, b) => {
      let comparison = 0
      
      switch (sortBy) {
        case 'name':
          const nameA = `${a.firstName || ''} ${a.lastName || ''}`.trim()
          const nameB = `${b.firstName || ''} ${b.lastName || ''}`.trim()
          comparison = nameA.localeCompare(nameB)
          break
        case 'id':
          comparison = (a.id || 0) - (b.id || 0)
          break
        case 'type':
          comparison = (a.type || '').localeCompare(b.type || '')
          break
        case 'status':
          comparison = (a.status || '').localeCompare(b.status || '')
          break
        case 'expectedStartTime':
          // Convert time strings to comparable format (handle both 12-hour and 24-hour)
          const timeA = a.expectedStartTime || ''
          const timeB = b.expectedStartTime || ''
          
          // Helper function to convert time to 24-hour format for comparison
          const convertTo24Hour = (timeStr) => {
            if (!timeStr) return '00:00'
            
            // If already in 24-hour format (HH:MM)
            if (/^\d{1,2}:\d{2}$/.test(timeStr)) {
              return timeStr.padStart(5, '0')
            }
            
            // If in 12-hour format (HH:MM AM/PM)
            const match = timeStr.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i)
            if (match) {
              let hour = parseInt(match[1])
              const minute = match[2]
              const period = match[3].toUpperCase()
              
              if (period === 'AM' && hour === 12) hour = 0
              if (period === 'PM' && hour !== 12) hour += 12
              
              return `${hour.toString().padStart(2, '0')}:${minute}`
            }
            
            return '00:00'
          }
          
          comparison = convertTo24Hour(timeA).localeCompare(convertTo24Hour(timeB))
          break
        default:
          comparison = 0
      }
      
      // Apply sort direction
      return sortDirection === 'asc' ? comparison : -comparison
    })

    return filtered
  }, [employees, searchTerm, filterType, sortBy, sortDirection, activeFilters])

  const getEmployeeTypeIcon = (type) => {
    return type === 'field' ? '🚛' : '🏭'
  }

  const getEmployeeTypeColor = (type) => {
    return type === 'field' ? 'text-blue-400' : 'text-green-400'
  }

  const handleEmployeeClick = (employee) => {
    navigate(`/employees/edit/${employee.id}`)
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <div className="text-gray-400">Loading employees...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-6">
          <div className="text-red-400 font-semibold mb-2">Error</div>
          <div className="text-red-300">{error}</div>
          <button
            onClick={fetchEmployees}
            className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-md transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Employee Management</h1>
        <p className="text-gray-400">View and manage all enrolled employees</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
          <div className="text-2xl font-bold text-blue-400">{employees.length}</div>
          <div className="text-sm text-gray-400">Total Employees</div>
        </div>
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
          <div className="text-2xl font-bold text-green-400">
            {employees.filter(emp => emp.type === 'field').length}
          </div>
          <div className="text-sm text-gray-400">Field Employees</div>
        </div>
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
          <div className="text-2xl font-bold text-purple-400">
            {employees.filter(emp => emp.type === 'warehouse').length}
          </div>
          <div className="text-sm text-gray-400">Warehouse Employees</div>
        </div>
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
          <div className="text-2xl font-bold text-yellow-400">
            {employees.filter(emp => emp.isActive !== false).length}
          </div>
          <div className="text-sm text-gray-400">Active Employees</div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
        <div className="flex flex-col gap-4">
          {/* Search */}
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by name, username, or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Employee Type Filter */}
          <div className="flex gap-4 items-center">
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:border-blue-500"
            >
              <option value="all">All Types</option>
              <option value="field">🚛 Field</option>
              <option value="warehouse">🏭 Warehouse</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="mb-4 text-gray-400">
        Showing {filteredAndSortedEmployees.length} of {employees.length} employees
      </div>

      {/* Employee Table */}
      <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-800">
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleFilterToggle('id')}
                >
                  <div className="flex items-center">
                    ID {sortBy === 'id' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleFilterToggle('name')}
                >
                  <div className="flex items-center">
                    Name {sortBy === 'name' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </div>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Username
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleFilterToggle('type')}
                >
                  <div className="flex items-center">
                    Type {sortBy === 'type' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleFilterToggle('expectedStartTime')}
                >
                  <div className="flex items-center">
                    Expected Time In {sortBy === 'expectedStartTime' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </div>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Phone
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleFilterToggle('status')}
                >
                  <div className="flex items-center">
                    Status {sortBy === 'status' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {filteredAndSortedEmployees.length === 0 ? (
                <tr>
                  <td colSpan="7" className="px-6 py-8 text-center text-gray-400">
                    {searchTerm || filterType !== 'all' 
                      ? 'No employees match your search criteria' 
                      : 'No employees found'
                    }
                  </td>
                </tr>
              ) : (
                filteredAndSortedEmployees.map((employee) => (
                  <tr 
                    key={employee.id} 
                    className="hover:bg-gray-800/50 transition-colors cursor-pointer"
                    onClick={() => handleEmployeeClick(employee)}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">
                      #{employee.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="text-sm font-medium text-white">
                          {(employee.firstName || '')} {(employee.lastName || '')}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      {employee.username || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className="mr-2">{getEmployeeTypeIcon(employee.type || 'warehouse')}</span>
                        <span className={`text-sm font-medium capitalize ${getEmployeeTypeColor(employee.type || 'warehouse')}`}>
                          {employee.type || 'warehouse'}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      <div className="flex items-center">
                        {employee.expectedStartTime ? (
                          <>
                            <span className="text-blue-400 mr-1">🕐</span>
                            <span>{employee.expectedStartTime}</span>
                          </>
                        ) : (
                          <span className="text-gray-500 italic">Not set</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      {employee.phoneNumber || employee.phone_number || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        employee.isActive !== false 
                          ? 'bg-green-900/20 text-green-400 border border-green-500/20' 
                          : 'bg-red-900/20 text-red-400 border border-red-500/20'
                      }`}>
                        {employee.isActive !== false ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Additional Info */}
      {filteredAndSortedEmployees.length > 0 && (
        <div className="mt-6 text-sm text-gray-400">
          <p>💡 Click on an employee row to view detailed information (feature coming soon)</p>
        </div>
      )}
    </div>
  )
}

export default EmployeeManagement
