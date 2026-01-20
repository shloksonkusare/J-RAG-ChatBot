import MessageCard from "./MessageCard";

interface GrammarCardProps {
  explanation: string;
  rule: string;
  usage: string;
  examples: string[];
  mistakes: string[];
  source: string;
}

const GrammarCard = ({
  explanation,
  rule,
  usage,
  examples,
  mistakes,
  source
}: GrammarCardProps) => {
  return (
    <MessageCard title="📘 Grammar Explanation">
      <section>
        <h3>Explanation</h3>
        <p>{explanation}</p>
      </section>

      <section>
        <h3>Rule</h3>
        <p>{rule}</p>
      </section>

      <section>
        <h3>Usage</h3>
        <p>{usage}</p>
      </section>

      <section>
        <h3>Examples</h3>
        <ul>
          {examples.map((ex, idx) => (
            <li key={idx}>{ex}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Common Mistakes</h3>
        <ul>
          {mistakes.map((m, idx) => (
            <li key={idx}>{m}</li>
          ))}
        </ul>
      </section>

      <footer className="source">📚 {source}</footer>
    </MessageCard>
  );
};

export default GrammarCard;
