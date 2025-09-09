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
    timeOut: '05:00 PM',
    breakIn: '03:30 PM',
    breakOut: null,
    status: 'On Duty'
  }
]

export const statusColors = {
  'On Duty': 'bg-green-500',
  'On Break': 'bg-gray-500',
  'Overtime': 'bg-blue-500',
  'Late': 'bg-red-500',
  'Undertime': 'bg-yellow-500'
}

export const getEmployeeStatus = (employee) => {
  if (employee.breakIn && !employee.breakOut) return 'On Break'
  return employee.status
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
    timeIn: '07:45 AM',
    timeOut: '04:15 PM',
    breakIn: '12:10 PM',
    breakOut: '12:50 PM',
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
    status: 'On Break'
  },
  {
    id: 103,
    firstName: 'Mia',
    lastName: 'Lee',
    timeIn: '06:55 AM',
    timeOut: '03:30 PM',
    breakIn: '11:30 AM',
    breakOut: '12:10 PM',
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
    status: 'Overtime'
  },
  {
    id: 105,
    firstName: 'Isabella',
    lastName: 'Walker',
    timeIn: '09:40 AM',
    timeOut: '05:00 PM',
    breakIn: '12:45 PM',
    breakOut: '01:25 PM',
    status: 'Late'
  }
]


