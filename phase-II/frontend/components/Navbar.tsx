'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { data: session } = authClient.useSession();

  const handleLogout = async () => {
    await authClient.signOut();
    router.push('/');
    router.refresh();
  };

  const menuItems = [
    {
      name: 'HOME',
      path: '/',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      )
    },
    {
      name: 'DASHBOARD',
      path: '/todo',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
        </svg>
      )
    },
    {
      name: 'TASKS',
      path: '/todo/tasks',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      )
    },
    {
      name: 'SETTINGS',
      path: '/todo/settings',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      )
    },
  ];

  return (
    <nav className="fixed left-0 top-0 h-full w-20 lg:w-24 glass border-r border-white/5 z-50 flex flex-col items-center py-8">
      {/* Refined Premium Logo Section */}
      <Link href="/" className="mb-12 group relative">
        <div className="w-12 h-12 primary-gradient rounded-xl flex items-center justify-center transition-all duration-500 group-hover:scale-110 shadow-[0_0_20px_rgba(16,185,129,0.3)] group-hover:shadow-[0_0_40px_rgba(16,185,129,0.5)] overflow-hidden">
          <div className="absolute inset-x-0 bottom-0 h-1/2 bg-black/10 backdrop-blur-[2px]"></div>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-zinc-950 relative z-10 transform group-hover:rotate-12 transition-transform duration-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <div className="absolute -inset-2 bg-primary/20 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
      </Link>

      {/* Main Nav Links */}
      <div className="flex-1 flex flex-col space-y-8 w-full px-2">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.name}
              href={item.path}
              className={`flex flex-col items-center justify-center py-3 rounded-2xl transition-all duration-300 group ${isActive ? 'bg-white/10 text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]' : 'text-zinc-500 hover:text-white hover:bg-white/5'}`}
            >
              <div className={`transition-transform duration-300 group-hover:scale-110 ${isActive ? 'text-primary' : ''}`}>
                {item.icon}
              </div>
              <span className={`text-[9px] font-bold mt-2 tracking-widest ${isActive ? 'text-white' : 'text-zinc-500'}`}>
                {item.name}
              </span>
            </Link>
          );
        })}
      </div>

      {/* Bottom Actions */}
      <div className="mt-auto flex flex-col items-center space-y-6 w-full px-2">
        {session ? (
          <>
            <button
              onClick={handleLogout}
              className="flex flex-col items-center justify-center py-3 w-full rounded-2xl text-zinc-500 hover:text-red-400 hover:bg-red-500/5 transition-all group"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span className="text-[9px] font-bold mt-2 tracking-widest">LOGOUT</span>
            </button>

            <div className="relative group p-0.5 rounded-full primary-gradient cursor-pointer">
              <div className="w-12 h-12 bg-zinc-950 rounded-full flex items-center justify-center text-xs font-bold text-white border-2 border-zinc-900 overflow-hidden shadow-lg group-hover:emerald-glow transition-all duration-300">
                {session.user.email?.[0].toUpperCase()}
              </div>
              <div className="absolute left-full ml-4 top-1/2 -translate-y-1/2 px-3 py-1 bg-white text-zinc-950 text-[10px] font-bold rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none transition-all duration-300 whitespace-nowrap z-100 shadow-xl">
                {session.user.email}
              </div>
            </div>
          </>
        ) : (
          <Link
            href="/login"
            className="flex flex-col items-center justify-center py-3 w-full rounded-2xl text-zinc-500 hover:text-primary hover:bg-primary/5 transition-all group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span className="text-[9px] font-bold mt-2 tracking-widest">LOGIN</span>
          </Link>
        )}
      </div>
    </nav>
  );
}
