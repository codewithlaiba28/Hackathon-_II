'use client';

import Link from "next/link";

export default function Footer() {
  const footerSections = [
    {
      title: 'Product',
      links: [
        { name: 'Features', href: '#features' },
        { name: 'How it works', href: '#' },
        { name: 'Pricing', href: '#' },
        { name: 'Integrations', href: '#' },
      ]
    },
    {
      title: 'Resources',
      links: [
        { name: 'Documentation', href: '#' },
        { name: 'API Reference', href: '#' },
        { name: 'Guides', href: '#' },
        { name: 'Blog', href: '#' },
      ]
    },
    {
      title: 'Company',
      links: [
        { name: 'About', href: '#about' },
        { name: 'Careers', href: '#' },
        { name: 'Security', href: '#' },
        { name: 'Legal', href: '#' },
      ]
    }
  ];

  return (
    <footer className="py-24 px-4 sm:px-6 lg:px-8 border-t border-white/5 relative bg-zinc-950/50 backdrop-blur-3xl">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12 lg:gap-16">
          <div className="lg:col-span-2 space-y-6">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 primary-gradient rounded-xl flex items-center justify-center emerald-glow">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-white font-bold text-xl tracking-tight">TodoPro</span>
            </Link>
            <p className="text-zinc-500 max-w-sm leading-relaxed">
              Experience the next generation of task management.
              Designed for performance, built for clarity. Elevate your
              productivity with our professional-grade tools.
            </p>
            <div className="flex space-x-4">
              {[1, 2, 3].map(i => (
                <button key={i} className="w-10 h-10 rounded-xl bg-zinc-900 border border-white/5 flex items-center justify-center text-zinc-500 hover:text-primary hover:border-primary/30 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.166 6.839 9.489.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12c0-5.523-4.477-10-10-10z" />
                  </svg>
                </button>
              ))}
            </div>
          </div>

          {footerSections.map((section) => (
            <div key={section.title} className="space-y-6">
              <h4 className="text-white font-bold text-sm uppercase tracking-widest">{section.title}</h4>
              <ul className="space-y-4">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <Link href={link.href} className="text-zinc-500 hover:text-primary transition-colors text-sm">
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-white/5 mt-20 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-zinc-600 text-sm italic">
            Developed by <span className="text-zinc-400">Laiba</span> for Hackathon II
          </p>
          <div className="flex space-x-8">
            <span className="text-zinc-600 text-sm uppercase tracking-[0.2em]">© 2026 TodoPro</span>
            <div className="flex space-x-6">
              <Link href="#" className="text-zinc-600 hover:text-zinc-400 text-xs transition-colors">Privacy</Link>
              <Link href="#" className="text-zinc-600 hover:text-zinc-400 text-xs transition-colors">Terms</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}