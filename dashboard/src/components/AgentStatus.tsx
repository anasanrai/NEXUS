'use client'

import { useEffect, useState } from 'react'

interface Status {
  status: string
  version: string
  tools_available: number
  session_id?: string
  execution_summary?: {
    total_tasks: number
    successful: number
    success_rate: number
  }
}

export default function AgentStatus() {
  const [status, setStatus] = useState<Status | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 5000) // Refresh every 5 seconds for live updates
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/status')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      console.error('Failed to fetch status:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    return status === 'Online' ? 'text-green-400' : 'text-red-400'
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">Agent Status</h2>
      {loading ? (
        <p className="text-slate-400">Loading status...</p>
      ) : status ? (
        <div className="space-y-3">
          <p className={`text-lg font-semibold ${getStatusColor(status.status)}`}>
            {status.status}
          </p>
          <div className="text-sm text-slate-400 space-y-1">
            <p>Version: {status.version}</p>
            <p>Tools: {status.tools_available}</p>
            {status.execution_summary && (
              <p>Success Rate: {(status.execution_summary.success_rate * 100).toFixed(0)}%</p>
            )}
          </div>
        </div>
      ) : (
        <p className="text-slate-400">Status unavailable</p>
      )}
    </div>
  )
}
