'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useChatStore } from '@/store/chat';
import { Conversation } from '@/types';
import { formatDate, truncateText } from '@/lib/utils';
import Link from 'next/link';

export default function Sidebar() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setIsLoading(true);
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/conversations`,
        {
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        }
      );

      if (!response.ok) {
        console.error('Failed to load conversations:', response.status);
        return;
      }

      const data = await response.json();
      setConversations(data.conversations || []);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const createNewConversation = () => {
    window.location.href = '/chat/new';
  };

  return (
    <aside className="w-64 border-r border-slate-200 bg-slate-50">
      <div className="flex h-full flex-col">
        <div className="p-4">
          <button
            onClick={createNewConversation}
            className="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
          >
            + New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3">
          {isLoading ? (
            <div className="py-4 text-center text-sm text-slate-500">
              Loading...
            </div>
          ) : conversations.length === 0 ? (
            <div className="py-4 text-center text-sm text-slate-500">
              No conversations yet
            </div>
          ) : (
            <div className="space-y-2">
              {conversations.map((conv) => (
                <Link
                  key={conv.id}
                  href={`/chat/${conv.id}`}
                  className="block rounded-lg px-3 py-2 text-sm hover:bg-slate-200"
                >
                  <div className="font-medium text-slate-900">
                    {truncateText(conv.title, 30)}
                  </div>
                  <div className="text-xs text-slate-500">
                    {formatDate(conv.updated_at)}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
