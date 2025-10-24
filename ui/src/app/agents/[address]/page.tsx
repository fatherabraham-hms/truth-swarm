import { AgentEvaluationOverview } from "@/components/agents/AgentEvaluationOverview";
import { Header } from "@/components/elements/Header";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";

interface PageProps {
  params: Promise<{ address: string }>;
}

export default async function AgentDetailPage({ params }: PageProps) {
  const { address } = await params;

  return (
    <>
      <Header />
      <MaxWidthWrapper>
        <div className="min-h-screen">
          <AgentEvaluationOverview address={address} />
        </div>
      </MaxWidthWrapper>
    </>
  );
}
