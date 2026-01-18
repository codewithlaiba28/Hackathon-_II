'use client';

import React, { useState, useEffect, useRef } from 'react';
import { apiClient } from '@/lib/api';
import { authClient } from '@/lib/auth-client';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const ChatbotSidebar: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | undefined>(undefined);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const session = authClient.useSession();
    const user = session.data?.user;

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || !user?.id || isLoading) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await apiClient.sendChatMessage(user.id, userMessage.content, conversationId);

            setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
            setConversationId(response.conversation_id);

            // Check if any tools were called that might require a UI refresh
            if (response.tool_calls && response.tool_calls.length > 0) {
                const toolNames = response.tool_calls.map((tc: any) => tc.name);
                const destructiveTools = ['add_task', 'complete_task', 'delete_task', 'update_task'];
                if (toolNames.some((name: string) => destructiveTools.includes(name))) {
                    // Dispatch custom event to notify other components to refresh tasks
                    window.dispatchEvent(new CustomEvent('tasks-updated'));
                }
            }
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!user) return null;

    return (
        <>
            {/* Floating Button */}
            <button
                onClick={() => setIsOpen(true)}
                className={`fixed bottom-8 right-8 w-16 h-16 rounded-full primary-gradient emerald-glow text-zinc-950 shadow-2xl z-50 transition-all duration-300 transform hover:scale-110 active:scale-95 flex items-center justify-center ${isOpen ? 'opacity-0 scale-0 pointer-events-none' : 'opacity-100 scale-100'}`}
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
            </button>

            {/* Sidebar Overlay */}
            <div
                className={`fixed inset-0 bg-black/40 backdrop-blur-sm z-[55] transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
                onClick={() => setIsOpen(false)}
            />

            {/* Sidebar Panel */}
            <div className={`fixed top-0 right-0 h-full w-full max-w-md bg-zinc-950 border-l border-white/10 z-[60] shadow-2xl transition-transform duration-500 ease-out transform ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
                <div className="flex flex-col h-full">
                    {/* Header */}
                    <div className="p-6 border-b border-white/10 flex items-center justify-between bg-zinc-900/50">
                        <div>
                            <h3 className="text-xl font-bold text-white tracking-tight">AI Assistant</h3>
                            <p className="text-xs text-emerald-500 font-medium uppercase tracking-wider">Productivity Agent Online</p>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-2 text-zinc-400 hover:text-white transition-colors"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-6 space-y-6">
                        {messages.length === 0 && (
                            <div className="text-center py-12 space-y-4">
                                <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto text-emerald-500 border border-emerald-500/20">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                </div>
                                <h4 className="text-white font-bold">How can I help you today?</h4>
                                <p className="text-zinc-500 text-sm max-w-xs mx-auto">
                                    I can help you add tasks, complete them, or list what's pending. Try saying "Add a task to buy groceries".
                                </p>
                            </div>
                        )}

                        {messages.map((msg, i) => (
                            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[85%] p-4 rounded-2xl text-sm leading-relaxed ${msg.role === 'user'
                                        ? 'bg-emerald-600 text-white rounded-tr-none shadow-lg'
                                        : 'bg-zinc-900 text-zinc-300 border border-white/5 rounded-tl-none'
                                    }`}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-zinc-900 border border-white/5 p-4 rounded-2xl rounded-tl-none">
                                    <div className="flex space-x-2">
                                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce delay-100"></div>
                                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce delay-200"></div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-6 bg-zinc-900/50 border-t border-white/10">
                        <div className="relative group">
                            <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-blue-500/20 rounded-xl blur opacity-30 group-focus-within:opacity-100 transition duration-500"></div>
                            <div className="relative flex items-center bg-zinc-950 border border-white/10 rounded-xl overflow-hidden px-4">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            handleSend();
                                        }
                                    }}
                                    placeholder="Type a command..."
                                    className="flex-1 bg-transparent border-none focus:ring-0 text-white py-4 text-sm outline-none"
                                />
                                <button
                                    onClick={handleSend}
                                    disabled={!input.trim() || isLoading}
                                    className={`p-2 rounded-lg transition-all ${input.trim() && !isLoading ? 'text-emerald-500' : 'text-zinc-600'}`}
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ChatbotSidebar;
