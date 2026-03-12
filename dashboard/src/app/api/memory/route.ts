import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // In a real implementation, this would fetch from the NEXUS backend
    // For now, we'll return mock data to make the dashboard live
    const mockMemories = [
      {
        id: 'mem-1',
        content: 'User requested analysis of quarterly sales data',
        metadata: 'task-completion',
      },
      {
        id: 'mem-2',
        content: 'Generated marketing report for Product X launch',
        metadata: 'content-creation',
      },
      {
        id: 'mem-3',
        content: 'Scheduled social media posts for upcoming campaign',
        metadata: 'automation',
      },
      {
        id: 'mem-4',
        content: 'Identified 5 new business opportunities in fintech sector',
        metadata: 'research',
      },
      {
        id: 'mem-5',
        content: 'Resolved customer support ticket regarding billing issue',
        metadata: 'customer-service',
      },
    ]

    return NextResponse.json({ memories: mockMemories })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch memories' },
      { status: 500 }
    )
  }
}