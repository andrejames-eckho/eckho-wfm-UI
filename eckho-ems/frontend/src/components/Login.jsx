import React, { useState } from 'react'
import { Target, Eye, EyeOff } from 'lucide-react'
// TODO: Replace with real auth API. For now, allow any non-empty admin or employee login.

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    
    if (!username.trim() || !password.trim()) {
      setError('Please enter both username and password')
      return
    }

    // Temporary logic: treat "admin/*" as admin, anything else as employee id lookup placeholder
    if (username.startsWith('admin')) {
      onLogin(username, password, 'admin')
      return
    }
    const maybeId = Number(username.split('.').pop())
    if (!Number.isNaN(maybeId)) {
      onLogin(username, password, 'employee', maybeId)
      return
    }
    setError('Invalid username or password')
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
      <div className="w-full max-w-md">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <Target className="w-10 h-10 text-white" />
            <h1 className="text-2xl font-semibold">ECKHO Workforce Management</h1>
          </div>
          <p className="text-gray-400">Sign in to your account</p>
        </div>

        {/* Login Form */}
        <div className="bg-gray-900 rounded-lg p-8 border border-gray-800">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                placeholder="Enter your username"
                autoComplete="username"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors pr-12"
                  placeholder="Enter your password"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="bg-red-900/50 border border-red-500 rounded-md p-3 text-red-200 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 border border-blue-500 rounded-md text-white font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              Sign In
            </button>
          </form>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 bg-gray-900 rounded-lg p-4 border border-gray-800">
          <h3 className="text-sm font-medium text-gray-300 mb-2">Demo Credentials:</h3>
          <div className="text-xs text-gray-400 space-y-1">
            <div className="font-medium text-blue-400">Admin:</div>
            <div>Username: admin</div>
            <div>Password: admin123</div>
            <div className="font-medium text-green-400 mt-2">Employee:</div>
            <div>Username: john.smith</div>
            <div>Password: emp123</div>
            <div className="text-gray-500 mt-1">Or use any employee's firstname.lastname</div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>© 2024 ECKHO Workforce Management. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}
