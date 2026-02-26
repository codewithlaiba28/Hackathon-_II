'use client';

import { authClient } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function SettingsPage() {
    const session = authClient.useSession();
    const router = useRouter();
    const user = session.data?.user;

    useEffect(() => {
        if (session.isPending) return;
        if (!session.data) {
            router.push('/login');
        }
    }, [session.isPending, session.data, router]);

    if (session.isPending) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="p-4 md:p-8 space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div className="text-zinc-500 text-sm font-medium mb-1">Productivity / Configuration</div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">Account Settings</h1>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-8">
                    <div className="glass-morphism rounded-3xl p-8 border border-white/5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[100px] -mr-32 -mt-32"></div>
                        <h3 className="text-xl font-bold text-white mb-8 relative z-10">Profile Information</h3>

                        <div className="space-y-6 relative z-10">
                            <div className="flex items-center space-x-6">
                                <div className="w-20 h-20 primary-gradient rounded-3xl flex items-center justify-center text-2xl font-bold text-zinc-950 emerald-glow">
                                    {user?.email?.[0].toUpperCase()}
                                </div>
                                <div>
                                    <h4 className="text-white font-bold text-lg">{user?.name || 'Pro User'}</h4>
                                    <p className="text-zinc-500 text-sm">{user?.email}</p>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Display Name</label>
                                    <input type="text" className="w-full px-5 py-3.5 bg-zinc-900 border border-white/5 rounded-2xl text-white placeholder-zinc-700 focus:outline-none focus:emerald-border-glow transition-all" defaultValue={user?.name || ''} placeholder="Your name" />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest ml-1">Email Address</label>
                                    <input type="email" className="w-full px-5 py-3.5 bg-zinc-950/50 border border-white/5 rounded-2xl text-zinc-500 cursor-not-allowed" defaultValue={user?.email || ''} disabled />
                                </div>
                            </div>
                        </div>

                        <div className="mt-12 flex justify-end">
                            <button className="px-8 py-3.5 primary-gradient text-zinc-950 font-bold rounded-2xl emerald-glow hover:scale-[1.02] active:scale-[0.98] transition-all">
                                Save Changes
                            </button>
                        </div>
                    </div>

                    <div className="glass-morphism rounded-3xl p-8 border border-white/5 space-y-8">
                        <h3 className="text-xl font-bold text-white">Preferences</h3>

                        <div className="space-y-4">
                            {[
                                { label: 'Push Notifications', desc: 'Receive alerts for upcoming deadlines.', active: true },
                                { label: 'Weekly Reports', desc: 'Get productivity insights in your inbox.', active: false },
                                { label: 'Dark Mode', desc: 'Sync interface with system settings.', active: true },
                            ].map(pref => (
                                <div key={pref.label} className="flex items-center justify-between p-4 bg-zinc-900/50 rounded-2xl border border-white/5">
                                    <div>
                                        <h5 className="font-bold text-white text-sm">{pref.label}</h5>
                                        <p className="text-zinc-500 text-xs">{pref.desc}</p>
                                    </div>
                                    <div className={`w-12 h-6 rounded-full relative transition-colors duration-300 cursor-pointer ${pref.active ? 'bg-primary' : 'bg-zinc-800'}`}>
                                        <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all duration-300 ${pref.active ? 'left-7' : 'left-1'}`}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="space-y-8">
                    <div className="glass-morphism rounded-3xl p-6 border border-white/5 bg-red-500/5">
                        <h3 className="text-lg font-bold text-red-400 mb-2">Danger Zone</h3>
                        <p className="text-zinc-500 text-xs mb-6">Permanently delete your account and all associated data. This action is irreversible.</p>
                        <button className="w-full py-3.5 rounded-2xl border border-red-500/20 text-red-500 text-sm font-bold hover:bg-red-500 hover:text-white transition-all">
                            Delete Account
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
