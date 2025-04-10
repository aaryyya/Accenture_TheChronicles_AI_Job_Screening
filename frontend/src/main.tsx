// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FolderUpload from './components/FolderUpload';
import ScheduleTest from './components/ScheduleTest';
import './index.css'; // if you use Tailwind or global styles

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/upload" element={<FolderUpload />} />
        <Route path="/schedule" element={<ScheduleTest />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
