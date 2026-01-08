'use client';

export default function Contact() {
    return (
        <section id="contact" className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
            <div className="max-w-7xl mx-auto relative z-10">
                <div className="text-center mb-16">
                    <h2 className="text-sm font-bold text-primary uppercase tracking-[0.3em] mb-4">Support</h2>
                    <h3 className="text-4xl md:text-5xl font-bold text-white tracking-tight">Let's talk productivity.</h3>
                </div>

                <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-5 gap-12 lg:gap-8 items-start">
                    <div className="lg:col-span-2 space-y-8">
                        <div className="glass-morphism p-6 rounded-3xl border border-white/5 space-y-3">
                            <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <h4 className="text-white font-bold">Email us</h4>
                            <p className="text-zinc-500 text-sm">Our team typically responds within 24 hours.</p>
                            <p className="text-primary font-medium text-sm">support@todopro.com</p>
                        </div>

                        <div className="glass-morphism p-6 rounded-3xl border border-white/5 space-y-3">
                            <div className="w-10 h-10 bg-accent/10 rounded-xl flex items-center justify-center text-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                                </svg>
                            </div>
                            <h4 className="text-white font-bold">Live Chat</h4>
                            <p className="text-zinc-500 text-sm">Available Monday to Friday, 9am - 5pm.</p>
                            <p className="text-accent font-medium text-sm">Start a conversation</p>
                        </div>
                    </div>

                    <div className="lg:col-span-3">
                        <form className="glass-morphism p-10 rounded-[2.5rem] border border-white/10 space-y-6 relative group overflow-hidden">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-primary/10 transition-colors"></div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Full Name</label>
                                    <input type="text" className="w-full px-5 py-3.5 bg-zinc-900 border border-white/5 rounded-2xl text-white placeholder-zinc-700 focus:outline-none focus:emerald-border-glow transition-all" placeholder="John Doe" />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Email</label>
                                    <input type="email" className="w-full px-5 py-3.5 bg-zinc-900 border border-white/5 rounded-2xl text-white placeholder-zinc-700 focus:outline-none focus:emerald-border-glow transition-all" placeholder="john@example.com" />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Subject</label>
                                <input type="text" className="w-full px-5 py-3.5 bg-zinc-900 border border-white/5 rounded-2xl text-white placeholder-zinc-700 focus:outline-none focus:emerald-border-glow transition-all" placeholder="How can we help?" />
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Message</label>
                                <textarea rows={4} className="w-full px-5 py-3.5 bg-zinc-900 border border-white/5 rounded-2xl text-white placeholder-zinc-700 focus:outline-none focus:emerald-border-glow transition-all" placeholder="Tell us more about your inquiry..."></textarea>
                            </div>

                            <button type="submit" className="w-full py-4 primary-gradient text-zinc-950 font-bold rounded-2xl emerald-glow hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center space-x-2">
                                <span>Send Message</span>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                </svg>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    );
}
