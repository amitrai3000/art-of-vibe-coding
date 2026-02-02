'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Message } from '@/types';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ModelSelector from './ModelSelector';
import { createClient } from '@/lib/supabase/client';
import { useChatStore } from '@/store/chat';

interface ChatInterfaceProps {
  conversationId: string;
}

export default function ChatInterface({ conversationId }: ChatInterfaceProps) {
  const {
    messages,
    currentConversationId,
    setCurrentConversation,
    setMessages,
    updateMessages,
    addMessage,
    clearMessages,
  } = useChatStore();
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  // Track the actual conversation ID (may differ from prop for new conversations)
  const actualConversationId = useRef<string | null>(conversationId === 'new' ? null : conversationId);
  // Track if we need to navigate after stream completes
  const pendingNavigationId = useRef<string | null>(null);
  const supabase = createClient();

  useEffect(() => {
    // Reset for new conversation
    if (conversationId === 'new') {
      actualConversationId.current = null;
      pendingNavigationId.current = null;
      setCurrentConversation(null);
      clearMessages();
      return;
    }

    actualConversationId.current = conversationId;
    const hasCachedMessages =
      currentConversationId === conversationId && messages.length > 0;

    setCurrentConversation(conversationId);
    if (!hasCachedMessages) {
      clearMessages();
    }

    loadMessages(conversationId, { preserveExisting: hasCachedMessages });
  }, [
    conversationId,
    currentConversationId,
    messages.length,
    clearMessages,
    setCurrentConversation,
  ]);

  const loadMessages = async (
    convId: string,
    options?: { preserveExisting?: boolean }
  ) => {
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/conversations/${convId}/messages`,
        {
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        }
      );

      if (!response.ok) {
        console.error('Failed to load messages:', response.status);
        return;
      }

      const data = await response.json();
      const nextMessages = data.messages || [];
      if (nextMessages.length === 0 && options?.preserveExisting) {
        return;
      }
      setMessages(nextMessages);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleSendMessage = async (content: string, provider: string) => {
    try {
      setIsLoading(true);

      // Add user message optimistically
      const userMessage: Message = {
        id: 'temp-' + Date.now(),
        conversation_id: actualConversationId.current || 'new',
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };
      addMessage(userMessage);

      // Get auth token
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        throw new Error('Not authenticated');
      }

      // Get current messages for context
      const currentMessages = [
        ...useChatStore.getState().messages,
        userMessage,
      ];

      // Stream response
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({
            conversation_id: actualConversationId.current,
            messages: currentMessages.map((m) => ({ role: m.role, content: m.content })),
            provider,
            stream: true,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      // Handle streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));

                // Capture conversation_id for new conversations
                if (data.conversation_id && !actualConversationId.current) {
                  actualConversationId.current = data.conversation_id;
                  pendingNavigationId.current = data.conversation_id;
                  setCurrentConversation(data.conversation_id);
                }

                if (data.content) {
                  assistantMessage += data.content;
                  // Update assistant message in real-time
                  updateMessages((prev) => {
                    const filtered = prev.filter(
                      (m) => !m.id.startsWith('temp-assistant')
                    );
                    return [
                      ...filtered,
                      {
                        id: 'temp-assistant-' + Date.now(),
                        conversation_id: actualConversationId.current || 'new',
                        role: 'assistant',
                        content: assistantMessage,
                        created_at: new Date().toISOString(),
                      },
                    ];
                  });
                }
              } catch (e) {
                // Ignore parse errors
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to send message. Please try again.');
      pendingNavigationId.current = null;
    } finally {
      setIsLoading(false);
      // Navigate to the actual conversation URL after stream completes
      if (pendingNavigationId.current) {
        const navId = pendingNavigationId.current;
        pendingNavigationId.current = null;
        router.replace(`/chat/${navId}`);
      }
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-slate-200 bg-white px-6 py-3">
        <ModelSelector />
      </div>
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>
      <div className="border-t border-slate-200 bg-white">
        <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}
