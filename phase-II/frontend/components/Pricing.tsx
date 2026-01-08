'use client';

import { useState } from 'react';

export default function Pricing() {
    const [activePlan, setActivePlan] = useState('Professional');

    const plans = [
        {
            name: 'Starter',
            price: '$0',
            description: 'Perfect for individuals just getting started.',
            features: ['Up to 10 tasks', 'Basic analytics', '7-day history', 'Mobile app access'],
            cta: 'Get Started'
        },
        {
            name: 'Professional',
            price: '$9',
            description: 'Ideal for power users and creators.',
            features: ['Unlimited tasks', 'Advanced insights', 'Unlimited history', 'Priority support', 'Custom themes'],
            cta: 'Go Pro'
        },
        {
            name: 'Enterprise',
            price: '$29',
            description: 'Built for teams that need control.',
            features: ['Team workspaces', 'Role management', 'Audit logs', 'SAML SSO', 'Dedicated manager'],
            cta: 'Contact Sales'
        }
    ];

    return (
        <section id="pricing" className="py-16 px-4 sm:px-6 lg:px-8 relative">
            <div className="max-w-7xl mx-auto relative z-10">
                <div className="text-center mb-20 space-y-4">
                    <div className="inline-block px-4 py-1.5 rounded-full bg-zinc-900 border border-white/5 text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4">
                        Plans & Access
                    </div>
                    <h3 className="text-4xl md:text-5xl font-black text-white tracking-tight">
                        Simple, <span className="text-gradient">transparent plans.</span>
                    </h3>
                    <p className="text-zinc-500 text-sm italic">Click a plan to select it</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-stretch">
                    {plans.map((plan) => {
                        const isActive = activePlan === plan.name;
                        return (
                            <div
                                key={plan.name}
                                onClick={() => setActivePlan(plan.name)}
                                className={`glass-morphism rounded-[2.5rem] p-10 border transition-all duration-500 relative cursor-pointer flex flex-col h-full
                  ${isActive
                                        ? 'border-primary/50 bg-primary/10 ring-2 ring-primary/20 z-20'
                                        : 'border-white/5 bg-zinc-900/40 hover:border-white/20'
                                    }`}
                            >
                                {isActive && (
                                    <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 py-1.5 primary-gradient rounded-full text-[10px] font-bold text-zinc-950 uppercase tracking-widest shadow-[0_0_20px_rgba(16,185,129,0.5)] z-30">
                                        Selected
                                    </div>
                                )}

                                <div className="mb-8 relative z-10">
                                    <h4 className={`text-xl font-bold mb-2 transition-colors ${isActive ? 'text-primary' : 'text-white'}`}>{plan.name}</h4>
                                    <div className="flex items-baseline space-x-1 mb-4">
                                        <span className={`text-4xl font-black transition-colors ${isActive ? 'text-white' : 'text-zinc-300'}`}>{plan.price}</span>
                                        <span className="text-zinc-500 text-sm">/month</span>
                                    </div>
                                    <p className="text-zinc-500 text-sm leading-relaxed">{plan.description}</p>
                                </div>

                                <ul className="space-y-4 mb-10 relative z-10 flex-1">
                                    {plan.features.map(feature => (
                                        <li key={feature} className={`flex items-center space-x-3 text-sm transition-colors ${isActive ? 'text-zinc-200' : 'text-zinc-400'}`}>
                                            <svg xmlns="http://www.w3.org/2000/svg" className={`h-5 w-5 shrink-0 ${isActive ? 'text-primary' : 'text-zinc-600'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                            </svg>
                                            <span>{feature}</span>
                                        </li>
                                    ))}
                                </ul>

                                <button className={`w-full py-4 rounded-2xl font-bold text-sm transition-all flex items-center justify-center space-x-2 relative z-10
                  ${isActive
                                        ? 'primary-gradient text-zinc-950 emerald-glow'
                                        : 'bg-zinc-900 border border-white/5 text-zinc-400 group-hover:text-white'
                                    }`}>
                                    <span>{plan.cta}</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                                    </svg>
                                </button>

                                {/* Internal Glow Effect for Active Plan */}
                                {isActive && (
                                    <div className="absolute inset-0 bg-primary/5 rounded-[2.5rem] -z-10 animate-pulse"></div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>
        </section>
    );
}
