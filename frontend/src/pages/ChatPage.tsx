import ChatInput from "../components/ChatInput";
import GrammarCard from "../components/GrammarCard";
import MistakeCard from "../components/MistakeCard";
import { useChat } from "../hooks/useChat";
import { parseAnswer } from "../utils/parseAnswer";
import "../styles/chat.css";

const ChatPage = () => {
  const { messages, loading, sendMessage } = useChat();

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Japanese Tutor 🇯🇵</h1>
      </header>

      <main className="chat-messages">
        {messages.map((msg) => {
          const parsed = parseAnswer(msg.content);

          if (parsed.type === "mistake") {
            return (
              <MistakeCard
                key={msg.id}
                explanation={parsed.data.explanation}
                rule={parsed.data.rule}
                corrected={parsed.data.corrected}
                incorrect={parsed.data.incorrect}
                correct={parsed.data.correct}
                source={parsed.data.source}
              />
            );
          }

          return (
            <GrammarCard
              key={msg.id}
              explanation={parsed.data.explanation}
              rule={parsed.data.rule}
              usage={parsed.data.usage}
              examples={parsed.data.examples}
              mistakes={parsed.data.mistakes}
              source={parsed.data.source}
            />
          );
        })}
      </main>

      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
};

export default ChatPage;
