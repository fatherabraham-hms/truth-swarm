"use client";

import * as React from "react";

import { Input } from "../ui/input";

export function ChatInteraction() {
  return (
    <div className="my-[30svh]">
      <div className="flex flex-col justify center items-center text-center">
        <span className=" text-2xl mb-8">Query Our Evaluator Agent</span>

        <Input
          className="[--radius:9999rem] max-w-xl p-8"
          placeholder="Send a message"
        />
      </div>
    </div>
  );
}
