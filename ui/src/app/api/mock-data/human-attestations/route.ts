import { NextResponse } from 'next/server';
import { getMockHumanAttestations } from '@/lib/mock-data-store';

export async function GET() {
  try {
    const attestations = getMockHumanAttestations();
    return NextResponse.json(attestations);
  } catch (error) {
    console.error('Error fetching mock human attestations:', error);
    return NextResponse.json(
      { error: 'Failed to fetch human attestations' },
      { status: 500 }
    );
  }
}
