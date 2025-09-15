const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const toCamel = (record) => ({
  id: record.id,
  employeeId: record.employee_id,
  date: new Date(record.date),
  expectedTimeIn: record.expected_time_in ?? null,
  expectedTimeOut: record.expected_time_out ?? null,
  timeIn: record.time_in ?? null,
  timeOut: record.time_out ?? null,
  breakIn: record.break_in ?? null,
  breakOut: record.break_out ?? null,
  status: record.status ?? null,
})

const toEmployee = (e) => ({
  id: e.id,
  firstName: e.first_name,
  lastName: e.last_name,
  expectedStartTime: e.expected_start_time ?? null,
})

export async function getEmployees() {
  const res = await fetch(`${API_BASE_URL}/employees/`)
  if (!res.ok) throw new Error('Failed to fetch employees')
  const data = await res.json()
  return data.map(toEmployee)
}

export async function getTimeRecords({ startDate, endDate, employeeId } = {}) {
  const params = new URLSearchParams()
  if (employeeId != null) params.set('employee_id', String(employeeId))
  if (startDate) params.set('start_date', startDate.toISOString().slice(0, 10))
  if (endDate) params.set('end_date', endDate.toISOString().slice(0, 10))
  const qs = params.toString()
  const res = await fetch(`${API_BASE_URL}/time-records/${qs ? `?${qs}` : ''}`)
  if (!res.ok) throw new Error('Failed to fetch time records')
  const data = await res.json()
  return data.map(toCamel)
}

export async function createTimeRecord(payload) {
  const snake = {
    employee_id: payload.employeeId,
    date: payload.date.toISOString().slice(0, 10),
    expected_time_in: payload.expectedTimeIn ?? null,
    expected_time_out: payload.expectedTimeOut ?? null,
    time_in: payload.timeIn ?? null,
    time_out: payload.timeOut ?? null,
    break_in: payload.breakIn ?? null,
    break_out: payload.breakOut ?? null,
    status: payload.status ?? null,
  }
  const res = await fetch(`${API_BASE_URL}/time-records/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(snake),
  })
  if (!res.ok) throw new Error('Failed to create time record')
  const data = await res.json()
  return toCamel(data)
}


