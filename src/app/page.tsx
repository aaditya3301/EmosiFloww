"use client";
import { GoogleGeminiEffect } from "@/components/ui/google-gemini-effect";
import Navbar from "@/components/ui/navbar";

export default function Home() {
  return (
    <div className="min-h-screen bg-black w-full dark:border dark:border-white/[0.1] rounded-md relative pt-20 overflow-clip">
      <Navbar
        isConnected={false}
        walletAddress=""
        isConnecting={false}
        handleConnectWallet={() => {}}
        formatAddress={(address: string) => address}
      />
      <GoogleGeminiEffect
        title="<EmosiFloww>"
        description=" The Decentralized Time-Capsule. Lock your digital assets and messages on-chain, encrypted for the future."
        className="sticky top-30"
      />
    </div>
  );
}
