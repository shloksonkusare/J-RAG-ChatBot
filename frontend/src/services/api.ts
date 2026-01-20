const API_BASE_URL = "http://127.0.0.1:8000";

export interface ChatResponse {
  answer: string;
  session_id: string;
}

export async function sendChatMessage(
  query: string,
  sessionId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query,
      session_id: sessionId
    })
  });

  if (!res.ok) {
    throw new Error("Failed to fetch response from backend");
  }

  return res.json();
}
