import MessageCard from "./MessageCard";

interface MistakeCardProps {
  explanation: string;
  rule: string;
  corrected: string[];
  incorrect: string;
  correct: string;
  source: string;
}

const MistakeCard = ({
  explanation,
  rule,
  corrected,
  incorrect,
  correct,
  source
}: MistakeCardProps) => {
  return (
    <MessageCard title="❌ Mistake Explanation">
      <section>
        <h3>Why this is incorrect</h3>
        <p>{explanation}</p>
      </section>

      <section>
        <h3>Correct Rule</h3>
        <p>{rule}</p>
      </section>

      <section>
        <h3>Corrected Examples</h3>
        <ul>
          {corrected.map((ex, idx) => (
            <li key={idx}>{ex}</li>
          ))}
        </ul>
      </section>

      <section className="contrast">
        <div className="incorrect">❌ {incorrect}</div>
        <div className="correct">✔ {correct}</div>
      </section>

      <footer className="source">📚 {source}</footer>
    </MessageCard>
  );
};

export default MistakeCard;
