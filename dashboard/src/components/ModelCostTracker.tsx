'use client'

import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

interface CostSummary {
  by_model: Record<string, number>
  total: number
}

export default function ModelCostTracker({ costSummary }: { costSummary?: CostSummary }) {
  const [data, setData] = useState<Array<{ name: string; cost: number }>>([])

  useEffect(() => {
    if (costSummary?.by_model) {
      const chartData = Object.entries(costSummary.by_model).map(([model, cost]) => ({
        name: model.split('/')[1] || model,
        cost: parseFloat(cost.toFixed(4)),
      }))
      setData(chartData)
    }
  }, [costSummary])

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">💰 Model Cost Tracker</h2>
      
      <div className="mb-6">
        <p className="text-slate-300">Total Cost (Session)</p>
        <p className="text-3xl font-bold text-green-400">
          ${costSummary?.total.toFixed(4) || '0.00'}
        </p>
      </div>

      {data.length > 0 ? (
        <div className="overflow-x-auto">
          <BarChart width={280} height={200} data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={80} />
            <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '6px', color: '#e2e8f0' }}
              formatter={(value) => `$${Number(value).toFixed(4)}`}
            />
            <Bar dataKey="cost" fill="#3b82f6" />
          </BarChart>
        </div>
      ) : (
        <p className="text-slate-400 text-sm">No cost data available</p>
      )}
    </div>
  )
}
