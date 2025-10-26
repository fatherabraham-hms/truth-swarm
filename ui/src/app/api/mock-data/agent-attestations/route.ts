import { NextResponse } from 'next/server';
import { getMockAgentAttestations } from '@/lib/mock-data-store';

export async function GET() {
  try {
    const attestations = getMockAgentAttestations();
    return NextResponse.json(attestations);
  } catch (error) {
    console.error('Error fetching mock agent attestations:', error);
    return NextResponse.json(
      { error: 'Failed to fetch agent attestations' },
      { status: 500 }
    );
  }
}
