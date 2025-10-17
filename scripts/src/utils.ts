import { ethers } from "ethers";

const SCHEMA_REGISTRY_ABI = [
  "event Registered(bytes32 indexed uid, address indexed registerer, SchemaRecord schema)",
] as const;

const SCHEMA_REGISTRY_INTERFACE = new ethers.Interface(SCHEMA_REGISTRY_ABI);

/**
 * Extracts the schema UID from a transaction receipt after schema registration
 * @param receipt - The transaction receipt from schemaRegistry.register()
 * @returns The schema UID if found, null otherwise
 */
export function extractSchemaUID(
  receipt: ethers.TransactionReceipt
): string | null {
  try {
    const decodedLogs = decodeLogs(receipt.logs);
    const registeredEvent = decodedLogs.find(
      (log) => log.type === "Schema Registered"
    );

    if (registeredEvent) {
      return registeredEvent.uid;
    }

    return null;
  } catch (error) {
    console.error("Error extracting schema UID:", error);
    return null;
  }
}

export function decodeLogs(logs: ReadonlyArray<ethers.Log>) {
  const decodedLogs = [] as any[];

  for (const log of logs) {
    try {
      // Check if this is a Schema Registry Registered event
      if (
        log.topics[0] ===
        SCHEMA_REGISTRY_INTERFACE.getEvent("Registered")!.topicHash
      ) {
        const decoded = SCHEMA_REGISTRY_INTERFACE.parseLog({
          topics: log.topics,
          data: log.data,
        });
        if (!decoded)
          throw new Error("Failed to decode Schema Registry Registered event");

        decodedLogs.push({
          type: "Schema Registered",
          contract: log.address,
          uid: decoded.args.uid,
          registerer: decoded.args.registerer,
          schema: decoded.args.schema,
        });
      } else {
        decodedLogs.push({
          type: "Unknown",
          address: log.address,
          topics: log.topics,
          data: log.data,
        });
      }
    } catch (error) {
      decodedLogs.push({ type: "Error decoding", log, error });
    }
  }

  return decodedLogs;
}

export function decodeError(errorOrData: any) {
  const errorData: string | undefined =
    typeof errorOrData === "string"
      ? errorOrData
      : errorOrData?.data ?? errorOrData?.error?.data;

  if (!errorData || errorData === "0x" || typeof errorData !== "string") {
    return { type: "No error data", selector: null, decoded: null };
  }

  const selector = errorData.slice(0, 10);

  // Try to decode with Schema Registry interface
  try {
    const decoded = SCHEMA_REGISTRY_INTERFACE.parseError(errorData);
    if (decoded) {
      return {
        type: "Decoded",
        contract: "SchemaRegistry",
        selector,
        errorName: decoded.name,
        signature: decoded.signature,
        args: decoded.args,
        decoded,
      };
    }
  } catch {
    // continue trying
  }

  try {
    const iError = new ethers.Interface(["error Error(string)"]);
    const parsed = iError.parseError(errorData);
    if (parsed)
      return { type: "Error(string)", selector, message: parsed.args[0] };
  } catch {}

  try {
    const iPanic = new ethers.Interface(["error Panic(uint256)"]);
    const parsed = iPanic.parseError(errorData);
    if (parsed)
      return {
        type: "Panic(uint256)",
        selector,
        code: parsed.args[0].toString(),
      };
  } catch {}

  return {
    type: "Unknown",
    selector,
    rawData: errorData,
    possibleParams: analyzeErrorParams(errorData),
  };
}

function analyzeErrorParams(errorData: string) {
  if (errorData.length <= 10) {
    return { analysis: "No parameters" };
  }

  const paramData = errorData.slice(10);
  const paramCount = paramData.length / 64;
  if (paramCount !== Math.floor(paramCount)) {
    return { analysis: "Invalid parameter length" };
  }

  const params = [] as any[];
  for (let i = 0; i < paramCount; i++) {
    const paramHex = paramData.slice(i * 64, (i + 1) * 64);
    const paramValue = BigInt("0x" + paramHex);
    if (
      paramHex.startsWith("000000000000000000000000") &&
      paramHex.length === 64
    ) {
      const address = "0x" + paramHex.slice(24);
      params.push({
        index: i,
        hex: "0x" + paramHex,
        uint256: paramValue.toString(),
        possibleAddress: address,
        type: "address-like",
      });
    } else {
      params.push({
        index: i,
        hex: "0x" + paramHex,
        uint256: paramValue.toString(),
        type: "uint256",
      });
    }
  }

  return { analysis: `${paramCount} parameters detected`, parameters: params };
}
