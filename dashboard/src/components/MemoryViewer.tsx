'use client'

import { useEffect, useState } from 'react'

interface Memory {
  id: string
  content: string
  metadata?: string
}

export default function MemoryViewer() {
  const [memories, setMemories] = useState<Memory[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMemories()
    const interval = setInterval(fetchMemories, 15000) // Refresh every 15 seconds for live updates
    return () => clearInterval(interval)
  }, [])

  const fetchMemories = async () => {
    try {
      const response = await fetch('/api/memory')
      const data = await response.json()
      setMemories(data.memories?.slice(0, 5) || [])
    } catch (error) {
      console.error('Failed to fetch memories:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">💭 Memory</h2>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading...</p>
      ) : memories.length === 0 ? (
        <p className="text-slate-400 text-sm">No memories stored</p>
      ) : (
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {memories.map((memory) => (
            <div key={memory.id} className="text-xs bg-slate-700/50 p-2 rounded">
              <p className="text-slate-200 line-clamp-2">{memory.content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
