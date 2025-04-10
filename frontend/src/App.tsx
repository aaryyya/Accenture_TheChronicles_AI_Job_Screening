// src/App.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

function App() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white w-full flex flex-col items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">AI Job Screening Tool</h1>
        <div className="flex flex-col space-y-4">
          <button
            onClick={() => navigate('/schedule')}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
          >
            Schedule Interview
          </button>
          <button
            onClick={() => navigate('/upload')}
            className="w-full px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors font-medium"
          >
            Upload CV Folder
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
