import { NextRequest, NextResponse } from 'next/server';
import { addNewEvaluatedAgent } from '@/lib/mock-data-store';
import { revalidatePath } from 'next/cache';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { agentAddress, evaluationData } = body;

    if (!agentAddress) {
      return NextResponse.json(
        { error: 'Agent address is required' },
        { status: 400 }
      );
    }

    // Add the new evaluated agent to mock data
    const result = addNewEvaluatedAgent(agentAddress, evaluationData);

    // Revalidate the dashboard page to refresh the data
    revalidatePath('/');

    return NextResponse.json({
      success: true,
      message: `Added new evaluated agent: ${result.agentInfo.name}`,
      agentInfo: result.agentInfo,
      attestation: result.attestation,
      timestamp: Date.now() // Add timestamp to help with cache invalidation
    });

  } catch (error) {
    console.error('Error adding new evaluated agent:', error);
    return NextResponse.json(
      { error: 'Failed to add new evaluated agent' },
      { status: 500 }
    );
  }
}
