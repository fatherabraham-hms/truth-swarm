import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import QueryContext from "@/context/QueryContext";
import WagmiContext from "@/context/WagmiContext";
import { BlockscoutContext } from "@/context/BlockscoutContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Truth Swarm",
  description:
    "Agentic verification & scoring mechanism for consumer protections",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <QueryContext>
          <WagmiContext>
            <BlockscoutContext>
              {children}
            </BlockscoutContext>
          </WagmiContext>
        </QueryContext>
      </body>
    </html>
  );
}
