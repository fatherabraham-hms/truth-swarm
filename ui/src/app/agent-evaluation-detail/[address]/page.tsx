import { Header } from "@/components/elements/Header";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { AgentEvaluationDetail } from "@/components/agent-evaluation-detail/AgentEvaluationDetail";

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
          <AgentEvaluationDetail address={address} />
        </div>
      </MaxWidthWrapper>
    </>
  );
}
