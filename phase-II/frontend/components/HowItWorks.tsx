'use client';

export default function HowItWorks() {
    const steps = [
        {
            number: '01',
            title: 'Sign Up',
            description: 'Create your account in seconds and get immediate access to your pro dashboard.',
            icon: (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
            )
        },
        {
            number: '02',
            title: 'Add Tasks',
            description: 'Break down your goals into actionable tasks using our intuitive quick-add interface.',
            icon: (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
            )
        },
        {
            number: '03',
            title: 'Track Progress',
            description: 'Monitor your completion rates and productivity analytics with real-time feedback.',
            icon: (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            )
        }
    ];

    return (
        <section id="how-it-works" className="py-16 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
            {/* Background Decorative Elements */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full max-w-4xl opacity-[0.03] pointer-events-none">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--primary)_0%,transparent_70%)]"></div>
            </div>

            <div className="max-w-7xl mx-auto relative z-10">
                <div className="text-center mb-24 space-y-4">
                    <div className="inline-block px-4 py-1.5 rounded-full bg-zinc-900 border border-white/5 text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4">
                        Workflow System
                    </div>
                    <h2 className="text-4xl md:text-5xl font-black text-white tracking-tight">
                        Designed for <span className="text-gradient">high-velocity teams.</span>
                    </h2>
                    <p className="text-zinc-500 max-w-2xl mx-auto text-lg">
                        Streamline your daily operations with our three-step integration process.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
                    {/* Connector Path (Desktop) */}
                    <div className="hidden md:block absolute top-10 left-[15%] right-[15%] h-0.5 pointer-events-none">
                        <div className="w-full h-full bg-linear-to-r from-transparent via-white/10 to-transparent"></div>
                    </div>

                    {steps.map((step, index) => (
                        <div
                            key={step.number}
                            className={`relative group animate-in fade-in slide-in-from-bottom-8 duration-700 fill-mode-both`}
                            style={{ animationDelay: `${index * 150}ms` }}
                        >
                            {/* Card Container */}
                            <div className="glass-morphism rounded-[2.5rem] p-8 border border-white/5 bg-zinc-900/40 hover:bg-zinc-900/60 hover:border-primary/20 transition-all duration-500 group">
                                <div className="relative mb-10">
                                    <div className="w-16 h-16 rounded-2xl bg-zinc-950 border border-white/10 flex items-center justify-center text-primary transition-all duration-500 group-hover:emerald-glow group-hover:primary-gradient group-hover:text-zinc-950 transform group-hover:scale-110 group-hover:-rotate-3">
                                        {step.icon}
                                    </div>
                                    <div className="absolute -top-4 -right-2 text-6xl font-black text-white/5 italic select-none pointer-events-none group-hover:text-primary/10 transition-colors duration-500">
                                        {step.number}
                                    </div>
                                </div>

                                <h4 className="text-2xl font-bold text-white mb-4 group-hover:text-primary transition-colors">{step.title}</h4>
                                <p className="text-zinc-500 text-sm leading-relaxed group-hover:text-zinc-400 transition-colors">
                                    {step.description}
                                </p>

                                {/* Visual Accent */}
                                <div className="mt-8 h-1 w-0 bg-primary group-hover:w-1/3 transition-all duration-700 rounded-full"></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
