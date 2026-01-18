'use client';

import React from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { authClient } from '@/lib/auth-client';

const OpenAIChatKitInterface: React.FC = () => {
    const [mounted, setMounted] = React.useState(false);
    const [inputValue, setInputValue] = React.useState('');
    const [isSending, setIsSending] = React.useState(false);

    React.useEffect(() => {
        setMounted(true);
    }, []);

    const chat = useChatKit({
        api: {
            url: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chatkit`,
            fetch: async (url: string | URL | Request, options: RequestInit | undefined) => {
                const session = await authClient.getSession();
                const token = session.data?.session.token;

                return fetch(url, {
                    ...options,
                    headers: {
                        ...options?.headers,
                        'Authorization': `Bearer ${token}`
                    }
                });
            },
            domainKey: '' // Required parameter for CustomApiConfig
        },
        theme: 'dark'
    } as any);

    const { control } = chat as any;

    const handleSend = async () => {
        if (!inputValue.trim() || isSending) return;

        setIsSending(true);
        const messageToSend = inputValue;
        setInputValue(''); // Clear input immediately for better UX

        try {
            if (chat?.sendUserMessage) {
                await chat.sendUserMessage({ text: messageToSend });
            } else {
                console.error('ChatKit sendUserMessage is not available');
                throw new Error('Chat interface not ready');
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            // Restore input on error
            setInputValue(messageToSend);
        } finally {
            setIsSending(false);
        }
    };

    if (!mounted) return null;

    return (
        <div className="h-full flex flex-col glass-morphism rounded-[2.5rem] overflow-hidden border border-white/10 mx-4 mb-4 shadow-[0_20px_50px_rgba(0,0,0,0.5)] bg-zinc-900/60 backdrop-blur-2xl relative" style={{ minHeight: '750px' }}>
            {/* Background Decorative Elements */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-500/50 to-transparent"></div>

            {/* Chat Messages Area */}
            <div className="flex-1 w-full h-full relative z-10 overflow-hidden">
                <ChatKit
                    control={control}
                    className="openai-chatkit w-full h-full"
                />
            </div>

            {/* Custom Premium Input Section */}
            <div className="p-6 relative z-20 bg-zinc-950/40 backdrop-blur-md border-t border-white/5">
                <div className="max-w-4xl mx-auto relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-blue-500/20 rounded-2xl blur opacity-30 group-focus-within:opacity-100 transition duration-500"></div>
                    <div className="relative flex items-center bg-zinc-900/80 border border-white/10 rounded-2xl overflow-hidden px-4 py-2 shadow-2xl transition-all duration-300 group-focus-within:border-emerald-500/30 group-focus-within:bg-zinc-900">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSend();
                                }
                            }}
                            placeholder="Type your command (e.g., 'Add a task to buy milk')..."
                            className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-zinc-500 py-3 text-sm outline-none"
                            disabled={isSending}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!inputValue.trim() || isSending}
                            className={`ml-4 p-2.5 rounded-xl transition-all duration-300 flex items-center justify-center ${inputValue.trim() && !isSending
                                ? 'bg-emerald-500 text-white shadow-[0_0_15px_rgba(16,185,129,0.4)] hover:scale-105 active:scale-95'
                                : 'bg-zinc-800 text-zinc-500 grayscale opacity-50'
                                }`}
                        >
                            {isSending ? (
                                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            ) : (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                                </svg>
                            )}
                        </button>
                    </div>
                </div>
                <div className="mt-3 text-center">
                    <p className="text-[10px] text-zinc-600 font-medium uppercase tracking-[0.2em]">Press Enter to send • AI Productivity Layer</p>
                </div>
            </div>

            <style jsx global>{`
                .openai-chatkit {
                    --chatkit-background: transparent;
                    --chatkit-foreground: #ffffff;
                    --chatkit-accent: #10b981;
                    --chatkit-border: rgba(255, 255, 255, 0.05);
                    --chatkit-font-family: 'Inter', system-ui, sans-serif;
                    --chatkit-secondary: rgba(255, 255, 255, 0.03);
                }

                /* IMPORTANT: Hide ChatKit's built-in composer completely */
                .openai-chatkit [data-testid="chat-input-container"],
                .openai-chatkit [data-testid="composer"],
                .openai-chatkit textarea,
                .openai-chatkit form {
                    display: none !important;
                    visibility: hidden !important;
                    height: 0 !important;
                    overflow: hidden !important;
                }

                /* Custom scrollbar for the chat */
                .openai-chatkit ::-webkit-scrollbar {
                    width: 6px;
                }
                .openai-chatkit ::-webkit-scrollbar-track {
                    background: transparent;
                }
                .openai-chatkit ::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                }
                .openai-chatkit ::-webkit-scrollbar-thumb:hover {
                    background: rgba(255, 255, 255, 0.2);
                }

                /* Message bubble refinements */
                .openai-chatkit [data-role="user"] {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                    border-radius: 20px 20px 4px 20px !important;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
                    border: none !important;
                }

                .openai-chatkit [data-role="assistant"] {
                    background: rgba(255, 255, 255, 0.05) !important;
                    backdrop-filter: blur(10px);
                    border-radius: 20px 20px 20px 4px !important;
                    border: 1px solid rgba(255, 255, 255, 0.1) !important;
                }
            `}</style>
        </div>
    );
};

export default OpenAIChatKitInterface;
