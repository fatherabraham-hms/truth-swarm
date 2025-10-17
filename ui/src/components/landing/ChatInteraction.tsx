"use client";

import * as React from "react";

import { Input } from "../ui/input";

export function ChatInteraction() {
  return (
    <div className="my-20 flex flex-col justify center items-center text-center">
      <span className="mt-20 mb-8 text-3xl">Query Our Evaluator Agent</span>

      <Input
        className="[--radius:9999rem] max-w-md p-6"
        placeholder="Send a message"
      />
    </div>
  );
}
