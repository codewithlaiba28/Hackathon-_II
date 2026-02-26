import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import ChatbotSidebar from "@/components/ChatbotSidebar";
import Script from "next/script";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TodoPro - Professional Task Management",
  description: "Manage your digital tasks with premium design and emerald focus.",
};

import { Toaster } from "@/components/ui/toaster";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <head>
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="afterInteractive"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground overflow-x-hidden`}
        suppressHydrationWarning={true}
      >
        <div className="flex min-h-screen">
          <Navbar />
          <div className="flex-1 flex flex-col min-w-0 min-h-screen">
            <main className="flex-1 lg:pl-24">
              {children}
            </main>
          </div>
        </div>
        <ChatbotSidebar />
        <Toaster />
      </body>
    </html>
  );
}
