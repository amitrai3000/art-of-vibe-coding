'use client';

interface AuthButtonProps {
  onSignOut: () => void;
}

export default function AuthButton({ onSignOut }: AuthButtonProps) {
  return (
    <button
      onClick={onSignOut}
      className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
    >
      Sign Out
    </button>
  );
}
