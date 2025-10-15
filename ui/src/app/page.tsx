import Image from "next/image";

import { Header } from "@/components/elements/Header";
import { Footer } from "@/components/elements/Footer";
import { MaxWidthWrapper } from "@/components/elements/MaxWidthWrapper";
import { FeatureAgentsCarousel } from "@/components/landing/FeatureAgentCarousel";


export default function Home() {
  return (
    <>
      <MaxWidthWrapper>
      <Header />
      <main className="min-h-screen text-center">
        <h1 className="text-7xl my-8">Truth Swarm</h1>

        {/** Hero Section */}
        <section className="grid grid-cols-2">
          <div className="flex flex-col">
            <span className="text-4xl mb-4">hero tag</span>
            <span className="mb-10">sub tag</span>
            <span>primary CTA</span>
          </div>
          <div className="flex items-center justify-center">
            <FeatureAgentsCarousel/>
          </div>

        </section>
        <section>

        </section>

      </main>
      <Footer />
      </MaxWidthWrapper>
    </>
  );
}
