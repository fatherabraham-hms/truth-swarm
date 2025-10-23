"use client";

import * as React from "react";
import ReactMarkdown from "react-markdown";
import { Input } from "../ui/input";
import {
  sendMessageToAgent,
  getSampleAgentAddress,
} from "@/actions/agentverse";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "agent";
  content: string;
  timestamp: number;
}

export function ChatInteraction() {
  const [messages, setMessages] = React.useState<Message[]>([]);
  const [input, setInput] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  const [sessionId, setSessionId] = React.useState<string>();
  const [isActive, setIsActive] = React.useState(false);
  const messagesContainerRef = React.useRef<HTMLDivElement>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when messages change
  React.useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: input.trim(),
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    if (!isActive) {
      setIsActive(true);
    }

    try {
      const agentAddressToEvaluate = userMessage.content;
      console.log("Sending to Evaluator Agent:", agentAddressToEvaluate);

      // Step 1: Send the evaluation request and get confirmation
      await sendToEvaluatorAgent(agentAddressToEvaluate);

      // Add a message indicating evaluation has started
      const pendingMessage: Message = {
        role: "agent",
        content: `Evaluation for agent \`${agentAddressToEvaluate.substring(
          0,
          20
        )}...\` has started. Please wait...`,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, pendingMessage]);

      // Step 2: Poll for the result
      const report = await pollForResult(agentAddressToEvaluate);

      // Step 3: Display the final report
      const reportContent = `
### Evaluation Report for ${report.evaluatedAgentAddress.substring(0, 20)}...

- **Final Score:** ${report.final_score}
- **Grade:** ${report.grade}
- **Attestation UID:** \`${
        report.attestation_uid
          ? report.attestation_uid.substring(0, 25)
          : "N/A"
      }...\`
`;

      const agentMessage: Message = {
        role: "agent",
        content: reportContent,
        timestamp: Date.now(),
      };

      // Replace the pending message with the final report
      setMessages((prev) => [...prev.slice(0, -1), agentMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);

      // Add error message
      const errorMessage: Message = {
        role: "agent",
        content: "Sorry, I encountered an error processing your message.",
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // Focus input field after agent responds
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  // Sending the target agent address to the backend evaluator agent
  async function sendToEvaluatorAgent(agentAddress: string) {
    try {
      const payload = await fetch("http://localhost:8000/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ agent_address: agentAddress }),
      });

      if (!payload.ok) {
        throw new Error(`Evaluation request failed: ${payload.statusText}`);
      }

      const data = await payload.json();
      if (data.status !== 'accepted') {
        throw new Error(data.message || "Agent did not accept the request.");
      }
      console.log("Evaluator Agent Response:", data);
      return data;
    } catch (error) {
      console.error("Error sending to evaluator agent:", error);
      throw error;
    }
  }
  async function pollForResult(agentAddress: string) {
    const MAX_ATTEMPTS = 10;
    const DELAY_MS = 3000; // 3 seconds

    for (let i = 0; i < MAX_ATTEMPTS; i++) {
      await new Promise(resolve => setTimeout(resolve, DELAY_MS));
      console.log(`Polling for result... Attempt ${i + 1}`);

      try {
        const response = await fetch("http://localhost:8000/get_report", {
          method: "POST", // uAgents @on_query uses POST
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ agent_address: agentAddress }),
        });

        if (!response.ok) continue; // Ignore failed polls

        const result = await response.json();
        if (result.grade !== "PENDING") {
          console.log("Final report received:", result);
          return result;
        }
      } catch (e) {
        console.error("Polling error:", e);
      }
    }

    throw new Error("Evaluation timed out. No result received from the agent.");
  }



  return (
    <div
      className={cn(
        "transition-all duration-300 flex flex-col",
        isActive ? "min-h-[80svh]" : "min-h-[60svh]"
      )}
    >
      {/* Chat messages area */}
      {isActive && (
        <div
          ref={messagesContainerRef}
          className="mt-20 flex-1 overflow-y-auto px-4 pb-6 space-y-4 max-h-[calc(80svh-12rem)]"
        >
          {messages.map((message, index) => (
            <div
              key={index}
              className={cn(
                "flex",
                message.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-[80%] rounded-2xl px-4 py-3",
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                )}
              >
                <div className="text-sm prose prose-sm dark:prose-invert max-w-none [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-2xl px-4 py-3 bg-muted">
                <p className="text-sm text-muted-foreground">
                  Agent is thinking...
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Input area - centered when inactive, bottom when active */}
      <div
        className={cn(
          "flex flex-col transition-all duration-300",
          isActive
            ? "justify-end items-stretch px-4 pb-4"
            : "justify-center items-center text-center flex-1"
        )}
      >
        {!isActive && (
          <span className="text-2xl mb-8">Query Our Evaluator Agent</span>
        )}

        <form onSubmit={handleSubmit} className={cn("max-w-xl w-full mx-auto")}>
          <Input
            ref={inputRef}
            className={cn(
              "[--radius:9999rem] transition-all",
              isActive ? "p-6" : "p-8"
            )}
            placeholder="Enter an agent address to evaluate"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
        </form>
      </div>
    </div>
  );
}
