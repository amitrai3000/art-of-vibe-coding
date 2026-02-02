import { create } from 'zustand';
import { AIProvider, Conversation, Message } from '@/types';

interface ChatState {
  conversations: Conversation[];
  currentConversationId: string | null;
  messages: Message[];
  selectedProvider: AIProvider;
  isLoading: boolean;

  setConversations: (conversations: Conversation[]) => void;
  setCurrentConversation: (conversationId: string | null) => void;
  setMessages: (messages: Message[]) => void;
  updateMessages: (updater: (messages: Message[]) => Message[]) => void;
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  setSelectedProvider: (provider: AIProvider) => void;
  setIsLoading: (loading: boolean) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  conversations: [],
  currentConversationId: null,
  messages: [],
  selectedProvider: 'claude',
  isLoading: false,

  setConversations: (conversations) => set({ conversations }),

  setCurrentConversation: (conversationId) =>
    set({ currentConversationId: conversationId }),

  setMessages: (messages) => set({ messages }),

  updateMessages: (updater) =>
    set((state) => ({ messages: updater(state.messages) })),

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  clearMessages: () => set({ messages: [] }),

  setSelectedProvider: (provider) => set({ selectedProvider: provider }),

  setIsLoading: (loading) => set({ isLoading: loading }),

  reset: () =>
    set({
      conversations: [],
      currentConversationId: null,
      messages: [],
      selectedProvider: 'claude',
      isLoading: false,
    }),
}));
