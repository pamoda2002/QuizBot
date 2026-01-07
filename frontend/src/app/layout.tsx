import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'QuizBot - AI Learning Companion',
  description: 'QuizBot - Your professional AI-powered quiz and learning assistant',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
