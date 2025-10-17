import React from "react";
import Link from "next/link";
import { buttonVariants } from "../ui/button";

export function Header() {
  return (
    <header>
      <nav className="w-full grid grid-cols-2 py-4">
        {/** Left grid */}
        <div className="flex justify-start items-center align-center">
          <span className="border border-b rounded-full p-2">TS</span>
          TruthSwarm
        </div>

        {/** Right grid */}
        <div className="flex items-center justify-end align-center">
          <Link
            href={"/docs"}
            className={buttonVariants({ size: "default", variant: "outline" })}
          >
            docs
          </Link>{" "}
          <Link
            href={"/connect"}
            className={buttonVariants({ size: "default", variant: "outline" })}
          >
            Connect Wallet
          </Link>
        </div>
      </nav>
    </header>
  );
}
