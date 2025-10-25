"use client";

import * as React from "react";
import ReactMarkdown from "react-markdown";
import { Input } from "../ui/input";
import { sendMessageToAgent } from "@/actions/agentverse";
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

    // Add user message to chat
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Activate chat mode on first message
    if (!isActive) {
      setIsActive(true);
    }

    try {
      // Send message to agent
      const { response, sessionId: newSessionId } = await sendMessageToAgent(
        userMessage.content,
        sessionId
      );

      // Update session ID
      if (newSessionId && !sessionId) {
        setSessionId(newSessionId);
      }

      // Add agent response to chat
      const agentMessage: Message = {
        role: "agent",
        content: response,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, agentMessage]);
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
            placeholder="Send a message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
        </form>
      </div>
    </div>
  );
}
