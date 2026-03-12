import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // In a real implementation, this would fetch from the NEXUS backend
    // For now, we'll return mock data to make the dashboard live
    const mockTasks = [
      {
        id: 'task-1',
        title: 'Process customer inquiries',
        status: 'completed',
        created_at: new Date(Date.now() - 3600000).toISOString(),
      },
      {
        id: 'task-2',
        title: 'Generate weekly report',
        status: 'in_progress',
        created_at: new Date(Date.now() - 1800000).toISOString(),
      },
      {
        id: 'task-3',
        title: 'Update documentation',
        status: 'pending',
        created_at: new Date(Date.now() - 900000).toISOString(),
      },
      {
        id: 'task-4',
        title: 'Review pull requests',
        status: 'pending',
        created_at: new Date(Date.now() - 300000).toISOString(),
      },
    ]

    return NextResponse.json({ tasks: mockTasks })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch tasks' },
      { status: 500 }
    )
  }
}