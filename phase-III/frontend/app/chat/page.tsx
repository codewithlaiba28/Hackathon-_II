'use client';

import React from 'react';
import OpenAIChatKitInterface from '@/components/OpenAIChatKitInterface';

export default function ChatPage() {
    return (
        <div className="min-h-screen bg-zinc-950 relative overflow-hidden flex flex-col">
            {/* Animated Background Orbs */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-emerald-900 rounded-full mix-blend-screen filter blur-[150px] opacity-[0.1] animate-pulse"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-zinc-800 rounded-full mix-blend-screen filter blur-[120px] opacity-[0.05]"></div>
            </div>

            <div className="flex-none p-8 z-10">
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <div>
                        <div className="text-emerald-500 text-[10px] font-bold uppercase tracking-[0.3em] mb-2">Neural Workspace</div>
                        <h1 className="text-4xl font-black text-white tracking-tight">AI Assistant</h1>
                        <p className="text-zinc-500 text-sm mt-1">Harnessing Gemini to amplify your productivity.</p>
                    </div>
                    <div className="hidden md:flex items-center space-x-4">
                        <div className="flex -space-x-2">
                            <div className="w-8 h-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-[10px] text-emerald-500 font-bold">G</div>
                        </div>
                        <div className="h-8 w-px bg-zinc-800"></div>
                        <span className="text-zinc-500 text-[10px] font-bold uppercase tracking-widest">v2.0 Beta</span>
                    </div>
                </div>
            </div>

            <div className="flex-1 max-w-7xl w-full mx-auto pb-8 z-10">
                <OpenAIChatKitInterface />
            </div>
        </div>
    );
}
