'use client';

export default function About() {
  return (
    <section id="about" className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16 relative z-10">
        <div className="flex-1 space-y-8">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="text-xs font-bold text-primary uppercase tracking-widest">Our Mission</span>
          </div>
          <h2 className="text-4xl md:text-6xl font-bold text-white tracking-tight leading-tight">
            Designed for those who <span className="text-gradient">build the future.</span>
          </h2>
          <p className="text-zinc-500 text-lg leading-relaxed max-w-xl">
            At TodoPro, we believe productivity is a craft. Every pixel and interaction is optimized
            to reduce cognitive load, allowing you to focus on what truly matters: your creative output.
          </p>
          <div className="grid grid-cols-2 gap-8 pt-4">
            <div>
              <div className="text-3xl font-bold text-white mb-1">99.9%</div>
              <div className="text-zinc-500 text-sm">Deployment Uptime</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-1">25ms</div>
              <div className="text-zinc-500 text-sm">Response Time</div>
            </div>
          </div>
        </div>

        <div className="flex-1 w-full max-w-xl">
          <div className="relative group">
            <div className="absolute -inset-1 bg-linear-to-r from-primary/30 to-accent/30 rounded-[3rem] blur-2xl opacity-20 group-hover:opacity-40 transition-opacity"></div>
            <div className="relative aspect-square glass-morphism rounded-[3rem] border border-white/10 flex items-center justify-center p-4 overflow-hidden">
              <img
                src="/about-visual.png"
                alt="Productivity Visualization"
                className="w-full h-full object-cover rounded-2xl opacity-80 group-hover:opacity-100 transition-opacity duration-700"
              />
              <div className="absolute inset-0 bg-linear-to-t from-zinc-950 via-transparent to-transparent opacity-40"></div>

              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-24 h-24 primary-gradient rounded-full flex items-center justify-center emerald-glow shadow-[0_0_50px_rgba(16,185,129,0.3)] transform group-hover:scale-110 transition-transform duration-500">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 text-zinc-950" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}