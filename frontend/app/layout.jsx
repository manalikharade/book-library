import '@/app/globals.css'
import Navbar from '@/components/Navbar'

export const metadata = {
  title: 'Book Library Management',
  description: 'Manage books, members, and borrowing records',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <Navbar />
        <div className="container mx-auto py-8">
          {children}
        </div>
      </body>
    </html>
  )
}
