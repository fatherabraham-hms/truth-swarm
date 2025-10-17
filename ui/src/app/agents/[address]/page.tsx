import { AgentEvaluationOverview } from "@/components/agents/AgentEvaluationOverview";

interface PageProps {
  params: Promise<{ address: string }>;
}

export default async function AgentDetailPage({ params }: PageProps) {
  const { address } = await params;

  return (
    <div className="min-h-screen">
      <AgentEvaluationOverview address={address} />
    </div>
  );
}
