// Dummy employee data
// Possible backend code
export const dummyEmployees = [
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
    timeOut: null,
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
    breakOut: null,
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
    timeOut: '06:00 PM',
    breakIn: '03:30 PM',
    breakOut: '4:30 PM',
    status: 'On Duty'
  }
]

export const statusColors = {
  'On Duty': 'bg-green-500',
  'On Break': 'bg-gray-500',
  'Overtime': 'bg-blue-500',
  'Late': 'bg-red-500',
  'Undertime': 'bg-yellow-500',
  'On Time': 'bg-teal-500',
  'No Record': 'bg-gray-600'
}

// Time helpers and rules for automatic status classification
const EXPECTED_START_TIME = '08:00 AM'
const EXPECTED_END_TIME = '05:00 PM'
const EXPECTED_WORK_MINUTES = 8 * 60 // 8 hours expected net work time
const GRACE_MINUTES = 15

const parseTimeToMinutes = (timeStr) => {
  if (!timeStr || typeof timeStr !== 'string') return null
  const [time, meridiem] = timeStr.trim().split(' ')
  if (!time || !meridiem) return null
  const [rawHour, rawMinute] = time.split(':')
  let hour = Number(rawHour)
  const minute = Number(rawMinute)
  if (Number.isNaN(hour) || Number.isNaN(minute)) return null
  const isPM = meridiem.toUpperCase() === 'PM'
  if (hour === 12) {
    hour = isPM ? 12 : 0
  } else if (isPM) {
    hour += 12
  }
  return hour * 60 + minute
}

// Returns positive minutes difference from start to end, wrapping across midnight if needed
const diffMinutesWrapMidnight = (startMin, endMin) => {
  if (startMin === null || endMin === null) return 0
  const ONE_DAY = 24 * 60
  const raw = endMin - startMin
  return raw >= 0 ? raw : raw + ONE_DAY
}

export const getEmployeeStatus = (employee) => {
  const timeInMin = parseTimeToMinutes(employee.timeIn)
  const timeOutMin = parseTimeToMinutes(employee.timeOut)
  const breakInMin = parseTimeToMinutes(employee.breakIn)
  const breakOutMin = parseTimeToMinutes(employee.breakOut)

  // Incomplete states first
  if (breakInMin !== null && breakOutMin === null) return 'On Break'
  if (timeInMin !== null && timeOutMin === null) return 'On Duty'

  // If we don't have complete required data, fallback to existing status
  if (timeInMin === null || timeOutMin === null || breakInMin === null || breakOutMin === null) {
    return employee.status
  }

  // Allow custom expected start time per employee (e.g., field employees)
  const expectedStartMin = parseTimeToMinutes(employee.expectedStartTime || EXPECTED_START_TIME)
  
  // For warehouse employees, use expected start/end times (8am-5pm) for status calculation
  if (!employee.expectedStartTime) {
    // Warehouse employees - use 8am-5pm schedule
    const expectedEndMin = parseTimeToMinutes('05:00 PM')
    
    if (expectedStartMin !== null && expectedEndMin !== null) {
      // Check if late (time in after 8:15am)
      const isLateBeyondGrace = timeInMin > (expectedStartMin + GRACE_MINUTES)
      
      // Check if left early (time out before 4:45pm)
      const isEarlyDeparture = timeOutMin < (expectedEndMin - GRACE_MINUTES)
      
      // Check if worked overtime (time out after 5:15pm)
      const isOvertime = timeOutMin > (expectedEndMin + GRACE_MINUTES)
      
      if (isLateBeyondGrace) return 'Late'
      if (isEarlyDeparture) return 'Undertime'
      if (isOvertime) return 'Overtime'
      return 'On Time'
    }
  } else {
    // Field employees - calculate based on actual time worked
    const breakDuration = diffMinutesWrapMidnight(breakInMin, breakOutMin)
    const grossDuration = diffMinutesWrapMidnight(timeInMin, timeOutMin)
    const netWorked = Math.max(0, grossDuration - breakDuration)
    
    // Calculate expected work time for field employees
    let expectedWorkMinutes = EXPECTED_WORK_MINUTES // Default 8 hours
    
    // Classification with grace:
    // - On Time if time in is <= expected start + 15 minutes (early is always On Time)
    // - On Time if net worked within ±15 minutes of expected work time
    // - Late only if time in exceeds expected start by more than 15 minutes
    // - Overtime if net worked > expected + 15 minutes
    // - Undertime if net worked < expected - 15 minutes

    const isLateBeyondGrace = expectedStartMin !== null && timeInMin > (expectedStartMin + GRACE_MINUTES)
    const withinWorkGrace = Math.abs(netWorked - expectedWorkMinutes) <= GRACE_MINUTES

    if (!isLateBeyondGrace && withinWorkGrace) return 'On Time'
    if (isLateBeyondGrace) return 'Late'
    if (netWorked > expectedWorkMinutes + GRACE_MINUTES) return 'Overtime'
    if (netWorked < expectedWorkMinutes - GRACE_MINUTES) return 'Undertime'
    return 'On Time'
  }

  return 'On Time'
}

export const formatDate = (date) => {
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Generate time records for the past 3 months
const generateTimeRecords = (employee, monthsBack = 3) => {
  const records = []
  const today = new Date()
  
  for (let monthOffset = 0; monthOffset < monthsBack; monthOffset++) {
    const currentMonth = new Date(today.getFullYear(), today.getMonth() - monthOffset, 1)
    const daysInMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate()
    
    for (let day = 1; day <= daysInMonth; day++) {
      const recordDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day)
      
      // Skip future dates
      if (recordDate > today) continue
      
      // Skip weekends (optional - you can remove this if employees work weekends)
      if (recordDate.getDay() === 0 || recordDate.getDay() === 6) continue
      
      // Generate random but realistic time data based on employee's expected start time
      const expectedStartTime = employee.expectedStartTime || '08:00 AM'
      const expectedTimeInMin = parseTimeToMinutes(expectedStartTime)
      
      let timeIn
      if (expectedTimeInMin !== null) {
        // Generate time within ±2 hours of expected start time
        const varianceMinutes = Math.floor(Math.random() * 240) - 120 // -2 to +2 hours
        const actualTimeInMin = expectedTimeInMin + varianceMinutes
        
        // Handle day rollover for night shifts
        const actualTimeInMinNormalized = actualTimeInMin < 0 ? actualTimeInMin + 24 * 60 : actualTimeInMin
        const actualHour = Math.floor(actualTimeInMinNormalized / 60) % 24
        const actualMinute = actualTimeInMinNormalized % 60
        
        timeIn = new Date(recordDate)
        timeIn.setHours(actualHour, actualMinute, 0, 0)
      } else {
        // Fallback to random time if expected start time is invalid
        const timeInHour = 7 + Math.floor(Math.random() * 3) // 7-9 AM
        const timeInMinute = Math.floor(Math.random() * 60)
        timeIn = new Date(recordDate)
        timeIn.setHours(timeInHour, timeInMinute, 0, 0)
      }
      
      // Calculate work hours based on employee type
      let workHours
      if (employee.expectedStartTime) {
        // Field employees - variable work hours
        workHours = 7.5 + Math.random() * 2 // 7.5-9.5 hours
      } else {
        // Warehouse employees - work until 5 PM
        const expectedEndTime = parseTimeToMinutes('05:00 PM')
        const timeInMinutes = parseTimeToMinutes(timeIn.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }))
        
        if (expectedEndTime !== null && timeInMinutes !== null) {
          // Calculate hours from time in to 5 PM, with some variance
          const baseWorkMinutes = expectedEndTime - timeInMinutes
          const varianceMinutes = Math.floor(Math.random() * 60) - 30 // ±30 minutes variance
          workHours = Math.max(4, (baseWorkMinutes + varianceMinutes) / 60) // Minimum 4 hours
        } else {
          workHours = 7.5 + Math.random() * 2 // Fallback
        }
      }
      
      const timeOut = new Date(timeIn.getTime() + workHours * 60 * 60 * 1000)
      
      const breakStart = new Date(timeIn.getTime() + 4 * 60 * 60 * 1000) // 4 hours after start
      const breakEnd = new Date(breakStart.getTime() + 30 * 60 * 1000) // 30 min break
      
      records.push({
        id: `${employee.id}-${recordDate.getTime()}`,
        employeeId: employee.id,
        date: new Date(recordDate),
        expectedTimeIn: employee.expectedStartTime || '08:00 AM',
        expectedTimeOut: employee.expectedStartTime ? null : '05:00 PM', // Only warehouse employees have expected end time
        timeIn: timeIn.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
        timeOut: timeOut.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
        breakIn: breakStart.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
        breakOut: breakEnd.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
        status: getEmployeeStatus({
          ...employee,
          timeIn: timeIn.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
          timeOut: timeOut.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
          breakIn: breakStart.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }),
          breakOut: breakEnd.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
        })
      })
    }
  }
  
  return records.sort((a, b) => b.date - a.date) // Sort by date descending (newest first)
}

// Additional dataset for Field employees
export const dummyFieldEmployees = [
  {
    id: 101,
    firstName: 'Ava',
    lastName: 'Martinez',
    timeIn: '11:30 PM',
    timeOut: null,
    breakIn: '12:10 AM',
    breakOut: '12:50 AM',
    expectedStartTime: '11:30 PM',
    status: 'On Duty'
  },
  {
    id: 102,
    firstName: 'Noah',
    lastName: 'Clark',
    timeIn: '09:10 AM',
    timeOut: '05:40 PM',
    breakIn: '01:00 PM',
    breakOut: null,
    expectedStartTime: '09:00 AM',
    status: 'On Break'
  },
  {
    id: 103,
    firstName: 'Mia',
    lastName: 'Lee',
    timeIn: '07:55 AM',
    timeOut: '03:30 PM',
    breakIn: '11:30 AM',
    breakOut: '12:10 PM',
    expectedStartTime: '07:00 AM',
    status: 'Undertime'
  },
  {
    id: 104,
    firstName: 'Ethan',
    lastName: 'Hernandez',
    timeIn: '10:05 AM',
    timeOut: '07:20 PM',
    breakIn: '02:15 PM',
    breakOut: '02:55 PM',
    expectedStartTime: '10:00 AM',
    status: 'Overtime'
  },
  {
    id: 105,
    firstName: 'Isabella',
    lastName: 'Walker',
    timeIn: '09:40 PM',
    timeOut: '06:30 AM',
    breakIn: '12:45 AM',
    breakOut: '01:25 AM',
    expectedStartTime: '09:30 PM',
    status: 'Late'
  }
]

// Generate time records for all employees
export const generateEmployeeTimeRecords = (employee) => {
  return generateTimeRecords(employee, 3) // 3 months of data
}

// Helper function to filter time records by date range
export const filterTimeRecordsByDateRange = (records, startDate, endDate) => {
  return records.filter(record => {
    const recordDate = new Date(record.date)
    return recordDate >= startDate && recordDate <= endDate
  })
}

// Helper function to group time records by week
export const groupTimeRecordsByWeek = (records) => {
  const grouped = {}
  
  records.forEach(record => {
    const date = new Date(record.date)
    const weekStart = new Date(date)
    weekStart.setDate(date.getDate() - date.getDay()) // Start of week (Sunday)
    weekStart.setHours(0, 0, 0, 0)
    
    const weekKey = weekStart.toISOString().split('T')[0]
    
    if (!grouped[weekKey]) {
      grouped[weekKey] = {
        weekStart,
        records: []
      }
    }
    
    grouped[weekKey].records.push(record)
  })
  
  return Object.values(grouped).sort((a, b) => b.weekStart - a.weekStart)
}

// Helper function to group time records by month
export const groupTimeRecordsByMonth = (records) => {
  const grouped = {}
  
  records.forEach(record => {
    const date = new Date(record.date)
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    
    if (!grouped[monthKey]) {
      grouped[monthKey] = {
        month: date.getMonth(),
        year: date.getFullYear(),
        records: []
      }
    }
    
    grouped[monthKey].records.push(record)
  })
  
  return Object.values(grouped).sort((a, b) => {
    if (a.year !== b.year) return b.year - a.year
    return b.month - a.month
  })
}

// Helper function to get employee time record for a specific date
export const getEmployeeTimeRecordForDate = (employee, targetDate) => {
  const allRecords = generateEmployeeTimeRecords(employee)
  const targetDateStr = targetDate.toDateString()
  
  return allRecords.find(record => {
    const recordDateStr = new Date(record.date).toDateString()
    return recordDateStr === targetDateStr
  })
}

// Helper function to get all employees with their time records for a specific date
export const getEmployeesWithTimeRecordsForDate = (employees, targetDate) => {
  return employees.map(employee => {
    const timeRecord = getEmployeeTimeRecordForDate(employee, targetDate)
    
    if (timeRecord) {
      // Return employee with time record data for the selected date
      return {
        ...employee,
        expectedTimeIn: timeRecord.expectedTimeIn,
        expectedTimeOut: timeRecord.expectedTimeOut,
        timeIn: timeRecord.timeIn,
        timeOut: timeRecord.timeOut,
        breakIn: timeRecord.breakIn,
        breakOut: timeRecord.breakOut,
        status: timeRecord.status,
        hasRecordForDate: true
      }
    } else {
      // Return employee without time record for the selected date
      return {
        ...employee,
        expectedTimeIn: employee.expectedStartTime || '08:00 AM',
        expectedTimeOut: employee.expectedStartTime ? null : '05:00 PM',
        timeIn: '-',
        timeOut: '-',
        breakIn: '-',
        breakOut: '-',
        status: 'No Record',
        hasRecordForDate: false
      }
    }
  })
}


