// frontend/src/app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { fetchAPI } from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [seminars, setSeminars] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }

    const loadDashboard = async () => {
      try {
        // Fetch everything concurrently
        const [userData, tasksData, seminarsData] = await Promise.all([
          fetchAPI('/api/me'),
          fetchAPI('/tasks/'),
          fetchAPI('/seminars/')
        ]);

        setUser(userData);
        setTasks(tasksData);
        setSeminars(seminarsData);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
        localStorage.removeItem('token');
        router.push('/');
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-lg font-medium text-gray-600">Loading Command Center...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-6xl space-y-8">
        
        {/* Header Section */}
        <div className="flex items-center justify-between rounded-xl bg-white p-6 shadow-sm border border-gray-100">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Logistics Hub</h1>
            <p className="mt-1 text-sm text-gray-500">
              Authenticated as: <span className="font-semibold text-gray-700">{user?.username}</span> ({user?.role})
            </p>
          </div>
          <button 
            onClick={handleLogout}
            className="rounded-md bg-red-50 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-100 transition-colors"
          >
            Sign Out
          </button>
        </div>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          
          {/* Tasks Section */}
          <div className="rounded-xl bg-white p-6 shadow-sm border border-gray-100">
            <h2 className="mb-4 text-xl font-semibold text-gray-800">Team Tasks</h2>
            {tasks.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No tasks assigned.</p>
            ) : (
              <ul className="space-y-3">
                {tasks.map(task => (
                  <li key={task.id} className="flex flex-col rounded-lg border border-gray-200 p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between">
                      <p className="font-medium text-gray-800">{task.title}</p>
                      <span className="text-xs font-medium uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-1 rounded-full">
                        {task.status}
                      </span>
                    </div>
                    {task.description && <p className="mt-2 text-sm text-gray-600">{task.description}</p>}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Seminars Section */}
          <div className="rounded-xl bg-white p-6 shadow-sm border border-gray-100">
            <h2 className="mb-4 text-xl font-semibold text-gray-800">Seminar Halls</h2>
            {seminars.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No halls configured.</p>
            ) : (
              <ul className="space-y-3">
                {seminars.map(hall => (
                  <li key={hall.id} className="flex items-center justify-between rounded-lg border border-gray-200 p-4 hover:bg-gray-50 transition-colors">
                    <div>
                      <p className="font-medium text-gray-800">{hall.name}</p>
                      <p className="text-xs text-gray-500 mt-1">Capacity: {hall.capacity} students</p>
                    </div>
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      hall.is_available 
                        ? 'bg-green-100 text-green-800 border border-green-200' 
                        : 'bg-red-100 text-red-800 border border-red-200'
                    }`}>
                      {hall.is_available ? 'Available' : 'Booked'}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}