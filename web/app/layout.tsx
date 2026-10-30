import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IT Support Copilot",
  description: "Get grounded answers to your workplace IT questions.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}