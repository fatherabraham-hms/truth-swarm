import { Header } from "@/components/elements/Header";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { HumanConfirmationDetail } from "@/components/human-confirmation-detail/HumanConfirmationDetail";

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
          <HumanConfirmationDetail uid={uid} />
        </div>
      </MaxWidthWrapper>
    </>
  );
}
