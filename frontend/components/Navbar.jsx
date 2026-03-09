'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navbar() {
  const pathname = usePathname()

  const isActive = (path) => pathname === path ? 'bg-blue-800' : 'hover:bg-blue-700'

  return (
    <nav className="bg-blue-600 text-white p-4 shadow-lg">
      <div className="container mx-auto">
        <h1 className="text-2xl font-bold mb-4">📚 Book Library Management</h1>
        <div className="flex gap-4 flex-wrap">
          <Link
            href="/"
            className={`px-4 py-2 rounded transition ${isActive('/')}`}
          >
            Dashboard
          </Link>
          <Link
            href="/books"
            className={`px-4 py-2 rounded transition ${isActive('/books')}`}
          >
            Books
          </Link>
          <Link
            href="/members"
            className={`px-4 py-2 rounded transition ${isActive('/members')}`}
          >
            Members
          </Link>
          <Link
            href="/borrowing"
            className={`px-4 py-2 rounded transition ${isActive('/borrowing')}`}
          >
            Borrowing/Returns
          </Link>
        </div>
      </div>
    </nav>
  )
}
