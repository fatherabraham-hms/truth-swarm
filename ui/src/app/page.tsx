import { Header } from "@/components/elements/Header";
import { Footer } from "@/components/elements/Footer";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { ChatInteraction } from "@/components/landing/ChatInteraction";
import { Dashboard } from "@/components/landing/Dashboard";

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
            <Dashboard />
          </section>
        </main>
        <Footer />
      </MaxWidthWrapper>
    </>
  );
}
