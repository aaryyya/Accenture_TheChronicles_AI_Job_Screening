// frontend/src/pages/ScheduleTest.tsx

import { useState } from "react";

export default function ScheduleTest() {
  const [loading, setLoading] = useState(false);
  const [eventLink, setEventLink] = useState("");
  const [error, setError] = useState("");
  const [authStatus, setAuthStatus] = useState<null | { authenticated: boolean; message: string }>(null);

  // Check authentication status on component mount
  const checkAuthStatus = async () => {
    try {
      const res = await fetch("http://localhost:8000/calendar/auth-status");
      const data = await res.json();
      setAuthStatus(data);
      
      if (!data.authenticated) {
        setError("Calendar authentication required. Please authenticate first.");
      }
    } catch (err) {
      console.error("Failed to check auth status:", err);
      setError("Failed to check authentication status. Please make sure the server is running.");
    }
  };

  // Authentication handler
  const handleAuth = async () => {
    setLoading(true);
    setError("");
    
    try {
      const res = await fetch("http://localhost:8000/calendar/auth");
      const data = await res.json();
      
      if (res.ok) {
        setAuthStatus({ authenticated: true, message: data.message });
        setError("");
      } else {
        setError(data.detail || "Authentication failed");
      }
    } catch (err) {
      console.error("Authentication failed:", err);
      setError("Authentication failed. Please check the server logs for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleSchedule = async () => {
    setLoading(true);
    setError("");
    setEventLink("");
    
    const payload = {
      candidate_email: "shreee752@gmail.com",
      interviewer_email: "aryampatil2005@gmail.com",
      start_time: "2025-04-17T15:00:00Z",
      end_time: "2025-04-17T15:30:00Z",
    };

    try {
      const res = await fetch("http://localhost:8000/calendar/schedule-interview/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      
      if (res.ok) {
        setEventLink(data.calendar_link || "No link returned");
      } else {
        setError(data.detail || "Failed to schedule interview");
      }
    } catch (err) {
      console.error("Scheduling failed:", err);
      setError("Scheduling failed. Please check the server logs for details.");
    } finally {
      setLoading(false);
    }
  };

  // Check auth status when component mounts
  if (authStatus === null) {
    checkAuthStatus();
  }

  return (
    <div className="min-h-screen bg-white w-full flex flex-col items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">Test Google Calendar Scheduling</h2>
        <div className="flex flex-col items-center space-y-6 w-full">
          {/* Authentication status */}
          {authStatus && (
            <div className={`w-full p-4 rounded-md border ${
              authStatus.authenticated 
                ? "bg-green-50 border-green-100 text-green-700" 
                : "bg-yellow-50 border-yellow-100 text-yellow-700"
            }`}>
              <p className="font-medium">{authStatus.message}</p>
            </div>
          )}
          
          {/* Error message */}
          {error && (
            <div className="bg-red-50 p-4 rounded-md border border-red-100 w-full">
              <p className="text-red-700 font-medium">{error}</p>
            </div>
          )}
          
          {/* Authentication button - show only if not authenticated */}
          {authStatus && !authStatus.authenticated && (
            <button
              onClick={handleAuth}
              className="w-full px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors font-medium"
              disabled={loading}
            >
              {loading ? "Authenticating..." : "Authenticate with Google Calendar"}
            </button>
          )}
          
          {/* Schedule button - only show if authenticated or no auth status check yet */}
          {(!authStatus || authStatus.authenticated) && (
            <button
              onClick={handleSchedule}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
              disabled={loading}
            >
              {loading ? "Scheduling..." : "Schedule Interview"}
            </button>
          )}
          
          {/* Success message */}
          {eventLink && (
            <div className="bg-green-50 p-4 rounded-md border border-green-100 w-full">
              <p className="text-green-700 font-medium mb-2">Event created successfully!</p>
              <a 
                href={eventLink} 
                target="_blank" 
                className="text-blue-600 hover:underline break-all"
              >
                {eventLink}
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
