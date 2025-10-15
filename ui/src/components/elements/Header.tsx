import React from "react";
import Link from "next/link";

export function Header() {
    return (
        <header>
            <nav className="w-full grid grid-cols-3 py-4">
                <div className="flex justify-start items-center align-center">
                    <span className="border border-b rounded-full p-2">TS</span>
                    TruthSwarm
                </div>
                <div>
                    <ol className="flex items-center justify-center space-x-4">
                        <li> <Link href={"/docs"}> Docs </Link> </li>
                        <li> <Link href={"/agents"}> Agents </Link> </li>
                        <li> <Link href={"/scoring"}> Scoring </Link> </li>
                    </ol>
                </div>
                <div className="flex items-center justify-end align-center">
                    <Link href={"/connect"}>Connect Wallet</Link>
                    
                </div>
            </nav>
        </header>
    );
}