'use client'

import { useEffect, useState } from 'react'

interface Task {
  id: string
  title: string
  status: string
  created_at?: string
}

export default function TaskFeed() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks()
    const interval = setInterval(fetchTasks, 60000) // Refresh every minute
    return () => clearInterval(interval)
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks')
      const data = await response.json()
      setTasks(data.tasks || [])
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-900 text-green-300'
      case 'in_progress':
        return 'bg-blue-900 text-blue-300'
      case 'pending':
        return 'bg-yellow-900 text-yellow-300'
      case 'failed':
        return 'bg-red-900 text-red-300'
      default:
        return 'bg-slate-700 text-slate-300'
    }
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">📋 Task Feed</h2>

      {loading ? (
        <p className="text-slate-400">Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p className="text-slate-400">No tasks yet</p>
      ) : (
        <div className="space-y-2">
          {tasks.slice(0, 10).map((task) => (
            <div key={task.id} className="flex items-center justify-between p-3 bg-slate-700/50 rounded">
              <div className="flex-1">
                <p className="text-white font-medium">{task.title}</p>
                {task.created_at && (
                  <p className="text-xs text-slate-400">
                    {new Date(task.created_at).toLocaleString()}
                  </p>
                )}
              </div>
              <span className={`px-3 py-1 rounded text-xs font-semibold ${getStatusColor(task.status)}`}>
                {task.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
