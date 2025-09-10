import React, { useState, useEffect, useMemo } from 'react'
import { Calendar, Filter, ChevronDown, ChevronUp } from 'lucide-react'
import { 
  getEmployeeStatus, 
  statusColors, 
  formatDate, 
  generateEmployeeTimeRecords,
  filterTimeRecordsByDateRange,
  groupTimeRecordsByWeek,
  groupTimeRecordsByMonth
} from '../utils/data'
import DateRangePicker from './DateRangePicker'

export default function EmployeeDetails({ employee }) {
  const [sortBy, setSortBy] = useState('date') // 'date', 'week', 'month'
  const [showDateRangePicker, setShowDateRangePicker] = useState(false)
  const [customDateRange, setCustomDateRange] = useState({ start: null, end: null })
  const [showAllRecords, setShowAllRecords] = useState(false)
  
  // Generate time records for the employee
  const allTimeRecords = useMemo(() => {
    return generateEmployeeTimeRecords(employee)
  }, [employee])

  // Filter records based on current view
  const filteredRecords = useMemo(() => {
    let records = allTimeRecords

    if (customDateRange.start && customDateRange.end) {
      records = filterTimeRecordsByDateRange(records, customDateRange.start, customDateRange.end)
    } else if (!showAllRecords) {
      // Show only past 30 days by default
      const thirtyDaysAgo = new Date()
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
      records = filterTimeRecordsByDateRange(records, thirtyDaysAgo, new Date())
    }

    return records
  }, [allTimeRecords, customDateRange, showAllRecords])

  // Group records based on sort option
  const groupedRecords = useMemo(() => {
    if (sortBy === 'week') {
      return groupTimeRecordsByWeek(filteredRecords)
    } else if (sortBy === 'month') {
      return groupTimeRecordsByMonth(filteredRecords)
    } else {
      return [{ records: filteredRecords }]
    }
  }, [filteredRecords, sortBy])

  const handleDateRangeChange = (startDate, endDate) => {
    setCustomDateRange({ start: startDate, end: endDate })
    setShowAllRecords(false)
  }

  const handleClearDateRange = () => {
    setCustomDateRange({ start: null, end: null })
    setShowAllRecords(false)
  }

  const handleShowAllRecords = () => {
    setShowAllRecords(true)
    setCustomDateRange({ start: null, end: null })
  }

  const formatWeekRange = (weekStart) => {
    const weekEnd = new Date(weekStart)
    weekEnd.setDate(weekEnd.getDate() + 6)
    return `${weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
  }

  const formatMonthYear = (month, year) => {
    const date = new Date(year, month)
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">
        Time Records for {employee.firstName} {employee.lastName}
      </h2>

      {/* Controls */}
      <div className="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
        <div className="flex flex-wrap items-center gap-4">
          {/* Sort Options */}
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-300">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-gray-700 text-white px-3 py-1 rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="date">Date</option>
              <option value="week">Week</option>
              <option value="month">Month</option>
            </select>
          </div>

          {/* Date Range Picker */}
          <button
            onClick={() => setShowDateRangePicker(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
          >
            <Calendar className="w-4 h-4" />
            <span>Custom Range</span>
          </button>

          {/* Show All Records */}
          <button
            onClick={handleShowAllRecords}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
          >
            Show All Records
          </button>

          {/* Clear Filters */}
          {(customDateRange.start || showAllRecords) && (
            <button
              onClick={handleClearDateRange}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors"
            >
              Clear Filters
            </button>
          )}
        </div>

        {/* Current Filter Status */}
        <div className="mt-3 text-sm text-gray-400">
          {customDateRange.start && customDateRange.end ? (
            <span>
              Showing records from {customDateRange.start.toLocaleDateString()} to {customDateRange.end.toLocaleDateString()}
            </span>
          ) : showAllRecords ? (
            <span>Showing all {allTimeRecords.length} records</span>
          ) : (
            <span>Showing past 30 days ({filteredRecords.length} records)</span>
          )}
        </div>
      </div>

      {/* Time Records */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-lg font-semibold mb-4">Time Records</h3>
        
        {groupedRecords.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            No time records found for the selected period.
          </div>
        ) : (
          <div className="space-y-6">
            {groupedRecords.map((group, groupIndex) => (
              <div key={groupIndex}>
                {/* Group Header */}
                {sortBy !== 'date' && (
                  <div className="mb-4 pb-2 border-b border-gray-700">
                    <h4 className="text-md font-semibold text-gray-200">
                      {sortBy === 'week' 
                        ? `Week of ${formatWeekRange(group.weekStart)}`
                        : formatMonthYear(group.month, group.year)
                      }
                      <span className="ml-2 text-sm text-gray-400">
                        ({group.records.length} records)
                      </span>
                    </h4>
                  </div>
                )}

                {/* Records Table */}
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
                      {group.records.map((record) => (
                        <tr key={record.id} className="border-b border-gray-800 hover:bg-gray-800">
                          <td className="py-3 px-4">{formatDate(record.date)}</td>
                          <td className="py-3 px-4">{record.timeIn}</td>
                          <td className="py-3 px-4">{record.timeOut}</td>
                          <td className="py-3 px-4">{record.breakIn} - {record.breakOut}</td>
                          <td className="py-3 px-4">
                            <span className={`px-3 py-1 rounded-full text-sm text-white ${statusColors[record.status]}`}>
                              {record.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Date Range Picker Modal */}
      <DateRangePicker
        isOpen={showDateRangePicker}
        onToggle={() => setShowDateRangePicker(false)}
        onDateRangeChange={handleDateRangeChange}
      />
    </div>
  )
}


