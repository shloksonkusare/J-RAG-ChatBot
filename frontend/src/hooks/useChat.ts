import { useState } from "react";
import { sendChatMessage } from "../services/api";

export interface ChatMessage {
  id: number;
  content: string;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text: string) => {
    setLoading(true);

    try {
      const response = await sendChatMessage(text, sessionId);

      setSessionId(response.session_id);
      setMessages((prev) => [
        ...prev,
        { id: Date.now(), content: response.answer }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const resetChat = () => {
    setMessages([]);
    setSessionId(undefined);
  };

  return {
    messages,
    loading,
    sendMessage,
    resetChat
  };
}
