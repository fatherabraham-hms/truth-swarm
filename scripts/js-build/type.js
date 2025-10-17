"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.encodingSchema = exports.schema = void 0;
exports.schema = `(
    string evaluatedAgentAddress,
    string evaluatorAgentAddress,
    uint256 timestamp,
    uint256 finalScore,
    uint8 overallConfidence,
    string grade,
    uint256 correctnessScore,
    uint8 correctnessConfidence,
    uint256 correctnessEffectiveScore,
    uint8 correctnessWeight,
    uint256 capabilitiesScore,
    uint8 capabilitiesConfidence,
    uint256 capabilitiesEffectiveScore,
    uint8 capabilitiesWeight,
    uint256 domainScore,
    uint8 domainConfidence,
    uint256 domainEffectiveScore,
    uint8 domainWeight,
    string detailsCID
  )`;
exports.encodingSchema = `string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID`;
