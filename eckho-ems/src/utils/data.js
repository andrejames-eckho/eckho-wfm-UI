// Dummy employee data
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
  'On Time': 'bg-teal-500'
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

  // Compute net worked minutes
  const breakDuration = diffMinutesWrapMidnight(breakInMin, breakOutMin)
  const grossDuration = diffMinutesWrapMidnight(timeInMin, timeOutMin)
  const netWorked = Math.max(0, grossDuration - breakDuration)

  // Allow custom expected start time per employee (e.g., field employees)
  const expectedStartMin = parseTimeToMinutes(employee.expectedStartTime || EXPECTED_START_TIME)
  // end time isn't used directly; we rely on net worked minutes with grace

  // Classification with grace:
  // - On Time if time in is <= expected start + 15 minutes (early is always On Time)
  // - On Time if net worked within ±15 minutes of expected 8h
  // - Late only if time in exceeds expected start by more than 15 minutes
  // - Overtime if net worked > expected + 15 minutes
  // - Undertime if net worked < expected - 15 minutes

  const isLateBeyondGrace = expectedStartMin !== null && timeInMin > (expectedStartMin + GRACE_MINUTES)
  const withinWorkGrace = Math.abs(netWorked - EXPECTED_WORK_MINUTES) <= GRACE_MINUTES

  if (!isLateBeyondGrace && withinWorkGrace) return 'On Time'
  if (isLateBeyondGrace) return 'Late'
  if (netWorked > EXPECTED_WORK_MINUTES + GRACE_MINUTES) return 'Overtime'
  if (netWorked < EXPECTED_WORK_MINUTES - GRACE_MINUTES) return 'Undertime'
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


