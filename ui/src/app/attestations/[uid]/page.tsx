import { Header } from "@/components/elements/Header";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { HumanAttestationDetail } from "@/components/attestations/HumanAttestationDetail";

interface PageProps {
  params: Promise<{ uid: string }>;
}

export default async function AttestationDetailPage({ params }: PageProps) {
  const { uid } = await params;

  return (
    <>
      <Header />
      <MaxWidthWrapper>
        <div className="min-h-screen">
          <HumanAttestationDetail uid={uid} />
        </div>
      </MaxWidthWrapper>
    </>
  );
}
