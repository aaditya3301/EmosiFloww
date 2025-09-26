import type { Metadata } from "next";
import { Quantico } from "next/font/google";
import "./globals.css";

const quantico = Quantico({
  variable: "--font-quantico",
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  title: "Tempris - Decentralized Time-Capsule Platform",
  description: "Create decentralized time-capsules using blockchain technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${quantico.variable} font-quantico antialiased bg-black text-white`}
      >
        {children}
      </body>
    </html>
  );
}
