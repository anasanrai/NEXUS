'use client'

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

export default function AgentStatus({ status }: { status: Status | null }) {
  if (!status) return null

  const successRate = status.execution_summary?.success_rate || 0
  const successPercentage = (successRate * 100).toFixed(0)

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Agent Status</h2>
        <span className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-green-400 font-medium">Online</span>
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-700/50 rounded p-4">
          <p className="text-slate-400 text-sm">Version</p>
          <p className="text-xl font-semibold text-white">{status.version}</p>
        </div>
        
        <div className="bg-slate-700/50 rounded p-4">
          <p className="text-slate-400 text-sm">Tools Available</p>
          <p className="text-xl font-semibold text-white">{status.tools_available}</p>
        </div>

        <div className="bg-slate-700/50 rounded p-4">
          <p className="text-slate-400 text-sm">Tasks Completed</p>
          <p className="text-xl font-semibold text-white">
            {status.execution_summary?.total_tasks || 0}
          </p>
        </div>

        <div className="bg-slate-700/50 rounded p-4">
          <p className="text-slate-400 text-sm">Success Rate</p>
          <p className="text-xl font-semibold text-white">{successPercentage}%</p>
        </div>
      </div>

      {status.session_id && (
        <div className="mt-4 pt-4 border-t border-slate-600">
          <p className="text-xs text-slate-400">Session ID</p>
          <p className="text-sm font-mono text-slate-300">{status.session_id}</p>
        </div>
      )}
    </div>
  )
}
