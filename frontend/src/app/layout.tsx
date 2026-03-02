import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Seafarer App",
  description: "Telegram Mini App for seafarers",
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
