'use client';

import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';

export default function Hero() {
  const router = useRouter();

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      router.push('/todo');
    } else {
      router.push('/login');
    }
  };

  const handleLearnMore = () => {
    const aboutSection = document.getElementById('about');
    if (aboutSection) {
      aboutSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6">
          Manage Your Tasks
          <span className="block bg-linear-to-r from-red-500 to-red-800 bg-clip-text text-transparent">
            Like a Pro
          </span>
        </h1>
        <p className="text-lg sm:text-xl md:text-2xl text-white/80 mb-10 max-w-3xl mx-auto">
          A simple, fast, and beautiful todo manager built with modern technology.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={handleGetStarted}
            className="bg-linear-to-r from-red-600 to-red-900 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-red-700 hover:to-red-950 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl hover:shadow-red-900/20"
          >
            Get Started
          </button>
          <button
            onClick={handleLearnMore}
            className="bg-white/10 backdrop-blur-md text-white px-8 py-4 rounded-lg text-lg font-semibold border border-white/20 hover:bg-white/20 transition-all duration-300"
          >
            Learn More
          </button>
        </div>
      </div>

      {/* Abstract wave shapes */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-linear-to-t from-red-900/20 to-transparent"></div>
    </section>
  );
}