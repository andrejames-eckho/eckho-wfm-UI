import React from 'react'
import { Target, User, LogOut } from 'lucide-react'

export default function Header({ showUserDropdown, onToggleUserDropdown, onSignOut, rightSlot }) {
  return (
    <div className="flex items-center justify-between p-6 border-b border-white">
      <div className="flex items-center space-x-3">
        <Target className="w-8 h-8 text-white" />
        <h1 className="text-xl font-semibold">ECKHO Workforce Management</h1>
      </div>
      <div className="flex items-center space-x-4">
        {rightSlot}
        <div className="relative">
          <button
            onClick={onToggleUserDropdown}
            className="p-2 hover:bg-gray-700 rounded-full transition-colors"
          >
            <User className="w-6 h-6" />
          </button>
          {showUserDropdown && (
            <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-md shadow-lg z-10">
              <button
                onClick={onSignOut}
                className="flex items-center w-full px-4 py-2 text-left hover:bg-gray-700 transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


