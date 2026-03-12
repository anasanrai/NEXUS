'use client'

import AgentStatus from '@/components/AgentStatus'
import TaskFeed from '@/components/TaskFeed'
import ModelCostTracker from '@/components/ModelCostTracker'
import MemoryViewer from '@/components/MemoryViewer'

export default function Home() {
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

      <main className="p-8">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <TaskFeed />
          </div>

          <div className="space-y-8">
            <AgentStatus />
            <ModelCostTracker />
            <MemoryViewer />
          </div>
        </div>
      </main>
    </div>
  )
}
