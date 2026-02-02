import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';

export default async function HomePage() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-slate-50 to-slate-100">
        <div className="max-w-md text-center">
          <h1 className="mb-4 text-4xl font-bold text-slate-900">
            AI Chat Platform
          </h1>
          <p className="mb-8 text-lg text-slate-600">
            Chat with multiple AI models in one place
          </p>
          <div className="space-y-4">
            <a
              href="/auth/signin"
              className="block rounded-lg bg-primary-600 px-6 py-3 font-semibold text-white hover:bg-primary-700"
            >
              Sign In
            </a>
            <a
              href="/auth/signup"
              className="block rounded-lg border border-slate-300 px-6 py-3 font-semibold text-slate-700 hover:bg-slate-50"
            >
              Create Account
            </a>
            <p className="text-sm text-slate-500">
              Supports Claude, OpenAI, and Gemini
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Redirect to chat if authenticated
  redirect('/chat/new');
}
