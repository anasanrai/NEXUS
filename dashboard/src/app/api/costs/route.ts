import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // In a real implementation, this would fetch from the NEXUS backend
    // For now, we'll return mock data to make the dashboard live
    const mockCostSummary = {
      by_model: {
        'minimax/minimax-m2.5': 0.0124,
        'z-ai/glm-5': 0.0087,
        'google/gemini-2.5-flash': 0.0213,
        'anthropic/claude-sonnet-4-5': 0.0042,
      },
      total: 0.0466,
    }

    return NextResponse.json(mockCostSummary)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch cost summary' },
      { status: 500 }
    )
  }
}