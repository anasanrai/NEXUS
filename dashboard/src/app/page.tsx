'use client'

import { useEffect, useState } from 'react'
import AgentStatus from '@/components/AgentStatus'
import TaskFeed from '@/components/TaskFeed'
import ModelCostTracker from '@/components/ModelCostTracker'
import MemoryViewer from '@/components/MemoryViewer'

export default function Home() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 30000) // Refresh every 30s
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-white">
            🤖 NEXUS Dashboard
          </h1>
          <p className="text-slate-400">Autonomous AI Operating System</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {loading ? (
          <div className="text-center text-white">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column */}
            <div className="lg:col-span-2 space-y-6">
              <AgentStatus status={status} />
              <TaskFeed />
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              <ModelCostTracker costSummary={status?.cost_summary} />
              <MemoryViewer />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
