# ECKHO Workforce Management System

A modern employee time tracking system built with Vite, React, and Tailwind CSS.

## Features

- **Employee Time Tracking Table**: View employee time records with first name, last name, time in/out, break times, and status
- **Status Color Coding**: Different colors for each status (On Duty-Green, On Break-Grey, Overtime-Blue, Late-Red, Undertime-Yellow)
- **Interactive Date Picker**: Click to change the date and view records for different days
- **User Dropdown Menu**: Access sign out functionality through the user icon
- **Employee Detail View**: Click on any employee row to view their detailed time records
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Modern dark interface matching the original design

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
   ```bash
   cd eckho-ems
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Usage

1. **View Employee Table**: The main page shows a table with all employee time records
2. **Change Date**: Click on the date picker to view records for different days
3. **View Employee Details**: Click on any employee row to see their detailed time records
4. **Sign Out**: Click on the user icon in the top-right corner and select "Sign Out"

## Technology Stack

- **Frontend**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Language**: JavaScript (JSX)

## Project Structure

```
eckho-ems/
├── src/
│   ├── App.jsx          # Main application component
│   ├── main.jsx         # Application entry point
│   └── index.css        # Global styles and Tailwind imports
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── tailwind.config.js   # Tailwind CSS configuration
├── postcss.config.js    # PostCSS configuration
└── vite.config.js       # Vite configuration
```

## Customization

The application uses dummy data for demonstration. To integrate with a real backend:

1. Replace the `dummyEmployees` array with API calls
2. Implement real authentication for the sign out functionality
3. Add data persistence for the date picker
4. Connect to a database for employee time records

## License

This project is for demonstration purposes.
