'use client';

import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export default function Hero() {
  const router = useRouter();
  const session = authClient.useSession();
  const isAuthenticated = !!session.data;

  const handleGetStarted = () => {
    if (isAuthenticated) {
      router.push('/todo');
    } else {
      router.push('/login');
    }
  };

  return (
    <section className="relative pt-16 lg:pt-24 pb-12 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        {/* Floating Batch */}
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 mb-8 animate-in fade-in slide-in-from-bottom-2 duration-700">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
          <span className="text-[10px] font-bold text-primary uppercase tracking-[0.2em]">v2.0 is now live</span>
        </div>

        {/* Main Heading */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-black text-white tracking-tight leading-[1.1] mb-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
          Finish your work <br />
          <span className="text-gradient">faster than ever.</span>
        </h1>

        {/* Subheading */}
        <p className="max-w-2xl mx-auto text-zinc-500 text-lg md:text-xl leading-relaxed mb-12 animate-in fade-in slide-in-from-bottom-6 duration-1000">
          Experience the next generation of task management. Professional grade tools,
          lightning fast interactions, and a design that respects your focus.
        </p>

        {/* Call to Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-20 animate-in fade-in slide-in-from-bottom-8 duration-1000">
          <button
            onClick={handleGetStarted}
            className="w-full sm:w-auto px-10 py-5 primary-gradient text-zinc-950 font-black rounded-2xl text-sm emerald-glow hover:scale-[1.05] active:scale-95 transition-all flex items-center justify-center space-x-3"
          >
            <span>START FOR FREE</span>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </button>
          <button className="w-full sm:w-auto px-10 py-5 bg-zinc-900 border border-white/5 text-zinc-400 font-bold rounded-2xl text-sm hover:text-white hover:bg-zinc-800 transition-all">
            VIEW DOCUMENTATION
          </button>
        </div>

        {/* Dashboard Preview Overlay */}
        <div className="relative max-w-5xl mx-auto px-4 perspective-[2000px] animate-in fade-in slide-in-from-bottom-10 duration-1000">
          <div className="absolute -inset-4 bg-primary/20 rounded-[3rem] blur-[120px] opacity-30 select-none pointer-events-none"></div>
          <div className="relative group rounded-[3rem] p-4 bg-zinc-900/50 backdrop-blur-3xl border border-white/10 shadow-2xl overflow-hidden transform-gpu transition-all duration-700 hover:rotate-x-2 max-h-[400px] md:max-h-[500px]">
            <div className="absolute inset-0 bg-linear-to-tr from-primary/5 via-transparent to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <img
              src="/hero-preview.png"
              alt="TodoPro Dashboard"
              className="w-full h-full object-cover object-top rounded-2xl shadow-inner border border-white/5 opacity-90 group-hover:opacity-100 transition-opacity"
            />

            {/* Fake UI Elements for polish */}
            <div className="absolute top-12 left-12 p-4 glass-morphism rounded-2xl border border-white/10 hidden md:block animate-bounce animation-duration-[3000ms]">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-primary shadow-[0_0_10px_rgba(16,185,129,1)]"></div>
                <span className="text-[10px] font-bold text-white uppercase tracking-widest">Live Syncing...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
