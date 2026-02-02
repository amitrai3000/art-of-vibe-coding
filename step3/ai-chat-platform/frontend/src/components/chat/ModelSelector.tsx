'use client';

import { useChatStore } from '@/store/chat';
import { AIProvider } from '@/types';

const PROVIDERS: { value: AIProvider; label: string; color: string }[] = [
  { value: 'claude', label: 'Claude', color: 'bg-orange-100 text-orange-800' },
  { value: 'openai', label: 'OpenAI', color: 'bg-green-100 text-green-800' },
  { value: 'gemini', label: 'Gemini', color: 'bg-blue-100 text-blue-800' },
];

export default function ModelSelector() {
  const { selectedProvider, setSelectedProvider } = useChatStore();

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm font-medium text-slate-700">Model:</span>
      <div className="flex space-x-2">
        {PROVIDERS.map((provider) => (
          <button
            key={provider.value}
            onClick={() => setSelectedProvider(provider.value)}
            className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
              selectedProvider === provider.value
                ? provider.color
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {provider.label}
          </button>
        ))}
      </div>
    </div>
  );
}
