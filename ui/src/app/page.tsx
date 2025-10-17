import { Header } from "@/components/elements/Header";
import { Footer } from "@/components/elements/Footer";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { ChatInteraction } from "@/components/landing/ChatInteraction";
import { EvaluatedAgentsOverview } from "@/components/landing/EvaluatdAgentsOverview";

export default function Home() {
  return (
    <>
      <MaxWidthWrapper>
        <Header />
        <main className="min-h-screen">
          {/** Chat interaction section */}
          <section>
            <ChatInteraction />
          </section>

          {/** Search Evaluated Agents */}
          <section>
            <EvaluatedAgentsOverview />
          </section>
        </main>
        <Footer />
      </MaxWidthWrapper>
    </>
  );
}
