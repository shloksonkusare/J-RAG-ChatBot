import "../styles/cards.css";

interface MessageCardProps {
  title: string;
  children: React.ReactNode;
}

const MessageCard = ({ title, children }: MessageCardProps) => {
  return (
    <div className="message-card">
      <h2 className="message-title">{title}</h2>
      <div className="message-content">{children}</div>
    </div>
  );
};

export default MessageCard;
