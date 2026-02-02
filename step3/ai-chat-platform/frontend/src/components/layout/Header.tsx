'use client';

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import AuthButton from '../auth/AuthButton';

export default function Header() {
  const router = useRouter();
  const supabase = createClient();

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  return (
    <header className="border-b border-slate-200 bg-white px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-slate-900">
            AI Chat Platform
          </h1>
        </div>
        <AuthButton onSignOut={handleSignOut} />
      </div>
    </header>
  );
}
