import { EvaluationScore } from "./type";

const EVALUATOR_ADDRESS =
  "agent1qw254tc8q3mcmrseem0pmhu2jd0j7urn2e9cd5tgcg88kmy9wkqhysksdwf";

export async function evaluateAgent(
  address: string,
  category: "good" | "average" | "bad" = "good"
) {
  // MOCK
  const agentWalletAddress = "0x"; // AGENT NO CONNECTION WITH WEB3
  const evaluationScore = generateEvaluationScore(address, category); // CALCULATED FROM TESTS
  const details = { ...evaluationScore, agentWalletAddress }; // TEST INFORMATION

  return { evaluationScore, details };
}

function generateEvaluationScore(
  address: string,
  category: "good" | "average" | "bad"
): EvaluationScore {
  // Generate component scores with some variation
  const correctnessScore = generateScore(category);
  const correctnessConfidence = generateConfidence(category);
  const correctnessWeight = 30;

  const capabilitiesScore = generateScore(category);
  const capabilitiesConfidence = generateConfidence(category);
  const capabilitiesWeight = 35;

  const domainScore = generateScore(category);
  const domainConfidence = generateConfidence(category);
  const domainWeight = 35;

  // Calculate effective scores (score * confidence / 10)
  const correctnessEffectiveScore = Math.round(
    (correctnessScore * correctnessConfidence) / 10
  );
  const capabilitiesEffectiveScore = Math.round(
    (capabilitiesScore * capabilitiesConfidence) / 10
  );
  const domainEffectiveScore = Math.round(
    (domainScore * domainConfidence) / 10
  );

  // Calculate final weighted score
  const finalScore = Math.round(
    (correctnessEffectiveScore * correctnessWeight +
      capabilitiesEffectiveScore * capabilitiesWeight +
      domainEffectiveScore * domainWeight) /
      100
  );

  // Overall confidence is average of component confidences
  const overallConfidence = Math.round(
    (correctnessConfidence + capabilitiesConfidence + domainConfidence) / 3
  );

  const grade = calculateGrade(finalScore);

  return {
    evaluatedAgentAddress: address,
    evaluatorAgentAddress: EVALUATOR_ADDRESS,
    timestamp: Math.floor(Date.now() / 1000),
    finalScore,
    overallConfidence,
    grade,
    correctnessScore,
    correctnessConfidence,
    correctnessEffectiveScore,
    correctnessWeight,
    capabilitiesScore,
    capabilitiesConfidence,
    capabilitiesEffectiveScore,
    capabilitiesWeight,
    domainScore,
    domainConfidence,
    domainEffectiveScore,
    domainWeight,
    detailsCID: "",
  };
}

/**
 * Generate random number in range with optional normal distribution
 * Uses Box-Muller transform for more realistic clustering around mean
 */
function randomInRange(min: number, max: number, useNormal = true): number {
  if (!useNormal) {
    return Math.random() * (max - min) + min;
  }
  // Box-Muller transform for normal distribution
  const u1 = Math.random();
  const u2 = Math.random();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  const mean = (min + max) / 2;
  const stdDev = (max - min) / 6; // ~99.7% within range
  return Math.max(min, Math.min(max, mean + z * stdDev));
}

/**
 * Generate score based on performance category
 * - good: 80-95 (most scores cluster around 87-88)
 * - average: 60-80 (most scores cluster around 70)
 * - bad: 30-60 (most scores cluster around 45)
 */
function generateScore(category: "good" | "average" | "bad"): number {
  switch (category) {
    case "good":
      return Math.round(randomInRange(80, 95));
    case "average":
      return Math.round(randomInRange(60, 80));
    case "bad":
      return Math.round(randomInRange(30, 60));
  }
}

/**
 * Generate confidence level (slightly correlated with score quality)
 * Higher performing agents tend to have more confident evaluations
 */
function generateConfidence(category: "good" | "average" | "bad"): number {
  switch (category) {
    case "good":
      return Math.round(randomInRange(7, 10));
    case "average":
      return Math.round(randomInRange(5, 8));
    case "bad":
      return Math.round(randomInRange(3, 7));
  }
}

/**
 * Calculate letter grade from numerical score
 */
function calculateGrade(score: number): string {
  if (score >= 93) return "A";
  if (score >= 90) return "A-";
  if (score >= 87) return "B+";
  if (score >= 83) return "B";
  if (score >= 80) return "B-";
  if (score >= 77) return "C+";
  if (score >= 73) return "C";
  if (score >= 70) return "C-";
  if (score >= 67) return "D+";
  if (score >= 63) return "D";
  if (score >= 60) return "D-";
  return "F";
}
