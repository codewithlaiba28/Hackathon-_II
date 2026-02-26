'use client';

import { useState } from 'react';

const faqs = [
    {
        question: "Is TodoPro really free to use?",
        answer: "Yes! Our Starter plan is completely free and includes all essential features forever. You can upgrade to Pro anytime for more advanced analytics and unlimited tasks."
    },
    {
        question: "How secure is my task data?",
        answer: "We use bank-grade encryption for all data transmissions and storage. Your tasks are private and accessible only by your authenticated account."
    },
    {
        question: "Can I collaborate with my team?",
        answer: "Team features are available in our Enterprise plan, which includes shared workspaces, real-time collaboration, and granular permissions."
    },
    {
        question: "Does it work offline?",
        answer: "TodoPro requires an internet connection for real-time sync across devices, but we are working on an offline-first mobile app coming later this year."
    }
];

export default function FAQ() {
    const [openIndex, setOpenIndex] = useState<number | null>(0);

    return (
        <section id="faq" className="py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-16 space-y-4">
                    <h2 className="text-sm font-bold text-primary uppercase tracking-[0.3em]">Support</h2>
                    <h3 className="text-4xl md:text-5xl font-bold text-white tracking-tight">Common questions.</h3>
                </div>

                <div className="space-y-4">
                    {faqs.map((faq, index) => (
                        <div
                            key={index}
                            className={`glass-morphism rounded-3xl border transition-all duration-300 overflow-hidden ${openIndex === index ? 'border-primary/20 bg-primary/5' : 'border-white/5 hover:border-white/10'}`}
                        >
                            <button
                                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                                className="w-full px-8 py-6 text-left flex items-center justify-between"
                            >
                                <span className="text-lg font-bold text-white">{faq.question}</span>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    className={`h-5 w-5 text-primary transition-transform duration-300 ${openIndex === index ? 'rotate-180' : ''}`}
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            <div
                                className={`px-8 transition-all duration-300 ease-in-out ${openIndex === index ? 'max-h-40 pb-6 opacity-100' : 'max-h-0 opacity-0 overflow-hidden'}`}
                            >
                                <p className="text-zinc-500 text-sm leading-relaxed">
                                    {faq.answer}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
