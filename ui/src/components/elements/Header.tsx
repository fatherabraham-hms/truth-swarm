"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useAccount, useConnect, useDisconnect, useBalance } from "wagmi";
import { metaMask } from "wagmi/connectors";
//import {injected } from "wagmi/connectors";
import { Wallet } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { buttonVariants } from "../ui/button";
import { cn, splitAddress } from "@/lib/utils";

export function Header() {
  const [mounted, setMounted] = useState(false);
  const { address, isConnected } = useAccount();
  const { connect } = useConnect();
  const { disconnect } = useDisconnect();

  const { data: balance } = useBalance({
    address: address,
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleClick = () => {
    if (isConnected) {
      disconnect();
    } else {
      //connect({ connector: injected() });  // instead of metaMask()
      connect({ connector: metaMask() });
    }
  };

  return (
    <header className="border-b">
      <nav className="px-4 py-4 flex items-center justify-between">
        {/** Left: Logo and Brand */}
        <Link
          href="/"
          className="flex items-center gap-3 hover:opacity-80 transition-opacity"
        >
          <Avatar className="h-9 w-9">
            <AvatarFallback className="bg-primary text-primary-foreground font-semibold">
              TS
            </AvatarFallback>
          </Avatar>
          <span className="text-xl font-semibold tracking-tight">
            Truth Swarm
          </span>
        </Link>

        {/** Right: Balance and Connect Button */}
        <div className="flex items-center gap-4">
          {mounted && isConnected && balance && (
            <div className="text-sm font-medium text-muted-foreground">
              {parseFloat(balance.formatted).toFixed(4)} {balance.symbol}
            </div>
          )}

          <button
            onClick={handleClick}
            className={cn(
              buttonVariants({ size: "default", variant: "outline" }),
              "hover:cursor-pointer"
            )}
          >
            <Wallet className="w-4 h-4 mr-2" />
            {mounted && isConnected && address ? (
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                {splitAddress(address)}
              </div>
            ) : (
              "Connect Wallet"
            )}
          </button>
        </div>
      </nav>
    </header>
  );
}
