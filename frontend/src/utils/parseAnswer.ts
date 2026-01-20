export interface ParsedGrammarAnswer {
  explanation: string;
  rule: string;
  usage: string;
  examples: string[];
  mistakes: string[];
  source: string;
}

export interface ParsedMistakeAnswer {
  explanation: string;
  rule: string;
  corrected: string[];
  incorrect: string;
  correct: string;
  source: string;
}

export function parseAnswer(answer: string) {
  const getSection = (label: string) => {
    const regex = new RegExp(`${label}:([\\s\\S]*?)(\\n\\w|$)`, "i");
    const match = answer.match(regex);
    return match ? match[1].trim() : "";
  };

  const source = getSection("Source");

  if (answer.includes("Mistake Explanation:")) {
    const corrected = getSection("Corrected Examples")
      .split("\n")
      .filter((l) => l.startsWith("-"))
      .map((l) => l.replace("-", "").trim());

    const contrast = getSection("Contrast")
      .split("\n")
      .map((l) => l.trim());

    return {
      type: "mistake",
      data: {
        explanation: getSection("Mistake Explanation"),
        rule: getSection("Correct Rule"),
        corrected,
        incorrect: contrast.find((l) => l.startsWith("❌"))?.replace("❌", "").trim() || "",
        correct: contrast.find((l) => l.startsWith("✔"))?.replace("✔", "").trim() || "",
        source
      }
    };
  }

  return {
    type: "grammar",
    data: {
      explanation: getSection("Grammar Explanation"),
      rule: getSection("Rule"),
      usage: getSection("Usage"),
      examples: getSection("Examples")
        .split("\n")
        .filter((l) => l.startsWith("-"))
        .map((l) => l.replace("-", "").trim()),
      mistakes: getSection("Common Mistakes")
        .split("\n")
        .filter((l) => l.startsWith("-"))
        .map((l) => l.replace("-", "").trim()),
      source
    }
  };
}
