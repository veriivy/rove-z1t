import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Flight Value Finder - Advanced Flight Recommendations',
  description: 'Discover the best flight deals with our advanced value-per-mile analysis. Compare airlines and find optimal redemption options for your travel.',
  keywords: 'flight recommendations, value per mile, airline rewards, travel deals, flight search',
  authors: [{ name: 'Flight Value Finder' }],
  robots: 'index, follow',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/favicon.ico" />
        <meta name="theme-color" content="#667eea" />
      </head>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
