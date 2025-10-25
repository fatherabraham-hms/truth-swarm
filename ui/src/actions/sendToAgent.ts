// app/actions/sendToAgent.ts
"use server";

import { v4 as uuidv4 } from "uuid";

type SendOptions = {
  waitForReply?: boolean; // whether to poll for a reply (short timeout)
  replyTimeoutMs?: number; // total timeout for polling (default 10_000ms)
};

/**
 * Server action: submit an envelope to Agentverse Mailbox and optionally poll for a reply.
 *
 * Expects these env vars:
 * - AGENTVERSE_BASE = https://agentverse.ai (or your custom host)
 * - AGENTVERSE_TOKEN = Bearer token
 * - AGENTVERSE_SENDER = your Bech32 address (so the agent can reply to you)
 * - AGENTVERSE_TARGET = target agent Bech32 address
 * - AGENTVERSE_SCHEMA_DIGEST = schema digest string for AIRequest (protocol)
 */
export async function sendToAgent(question: string, opts: SendOptions = {}) {
  const { waitForReply = false, replyTimeoutMs = 10000 } = opts;

  const BASE = process.env.AGENTVERSE_BASE ?? "https://agentverse.ai";
  const TOKEN = process.env.AGENTVERSE_API_KEY;
  const SENDER = process.env.AGENTVERSE_SENDER; // MAILBOX ADDRESS
  const TARGET = process.env.AGENTVERSE_TARGET;
  const SCHEMA_DIGEST = process.env.AGENTVERSE_SCHEMA_DIGEST;

  if (!TOKEN || !SENDER || !TARGET || !SCHEMA_DIGEST) {
    throw new Error("Missing required Agentverse environment variables.");
  }

  // Build payload JSON for AIRequest
  const payloadJson = JSON.stringify({ question });
  // base64 encode (Node)
  const payloadB64 = Buffer.from(payloadJson).toString("base64");

  const envelope = {
    version: 1,
    sender: SENDER,
    target: TARGET,
    session: uuidv4(),
    schema_digest: SCHEMA_DIGEST,
    payload: payloadB64,
  };

  // submit envelope
  const submitResp = await fetch(`${BASE}/v1/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${TOKEN}`,
    },
    body: JSON.stringify(envelope),
  });

  if (!submitResp.ok) {
    const text = await submitResp.text().catch(() => null);
    throw new Error(
      `Agentverse submit failed: ${submitResp.status} ${
        submitResp.statusText
      } ${text ?? ""}`
    );
  }

  const submitJson = await submitResp.json();

  // If not waiting for a reply, return submission result immediately
  if (!waitForReply) {
    return { submitted: true, submitResult: submitJson };
  }

  // Polling loop to check mailbox for responses addressed to our SENDER
  // NOTE: Polling is OK for short waits during user interactions; prefer webhooks for production.
  const start = Date.now();
  let delay = 500; // initial backoff
  const maxDelay = 2000;

  while (Date.now() - start < replyTimeoutMs) {
    // list mailbox messages for recipient = SENDER
    // Adjust endpoint / query to match your Agentverse mailbox list API
    const listUrl = new URL(`${BASE}/v1/mailbox/messages`);
    listUrl.searchParams.set("recipient", SENDER);
    // optionally filter by session id or target to avoid unrelated messages

    const listResp = await fetch(listUrl.toString(), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${TOKEN}`,
      },
    });

    if (!listResp.ok) {
      // non-fatal: wait and try again
      await new Promise((r) => setTimeout(r, delay));
      delay = Math.min(maxDelay, delay * 1.6);
      continue;
    }

    const listJson = await listResp.json().catch(() => null);
    if (listJson && Array.isArray(listJson.items)) {
      // iterate items and try to find a reply targeted at this session/sender/target
      for (const item of listJson.items) {
        try {
          // Agentverse mailbox shapes vary — common pattern: item.envelope.payload
          const envelopePayloadB64 =
            item?.envelope?.payload ?? item?.payload ?? null;
          if (!envelopePayloadB64) continue;

          const raw = Buffer.from(envelopePayloadB64, "base64").toString(
            "utf8"
          );
          const parsed = JSON.parse(raw);

          // If this looks like AIResponse (contains 'text'), return it.
          if (parsed?.text) {
            return {
              submitted: true,
              submitResult: submitJson,
              reply: parsed,
              rawEnvelope: item,
            };
          }
        } catch (e) {
          // skip malformed item
          continue;
        }
      }
    }

    // wait then retry
    await new Promise((r) => setTimeout(r, delay));
    delay = Math.min(maxDelay, Math.floor(delay * 1.6));
  }

  // timed out waiting for reply
  return {
    submitted: true,
    submitResult: submitJson,
    reply: null,
    timedOut: true,
  };
}
