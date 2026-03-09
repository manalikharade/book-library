'use client'

import { useState, useEffect } from 'react'
import { borrowingApi, bookApi, memberApi } from '@/lib/api'
import BorrowForm from '@/components/BorrowForm'
import ReturnForm from '@/components/ReturnForm'
import BorrowingTable from '@/components/BorrowingTable'

export default function BorrowingPage() {
  const [borrowings, setBorrowings] = useState([])
  const [activeBorrowings, setActiveBorrowings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showBorrowForm, setShowBorrowForm] = useState(false)
  const [showReturnForm, setShowReturnForm] = useState(false)
  const [books, setBooks] = useState([])
  const [members, setMembers] = useState([])

  useEffect(() => {
    fetchAllData()
  }, [])

  const fetchAllData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [borrowingsRes, booksRes, membersRes, activeRes] = await Promise.all([
        borrowingApi.getAllBorrowings(),
        bookApi.getAllBooks(),
        memberApi.getAllMembers(),
        borrowingApi.getActiveBorrowings(),
      ])
      setActiveBorrowings(activeRes.data)
      setBorrowings(borrowingsRes.data)
      setBooks(booksRes.data)
      setMembers(membersRes.data)
    } catch (err) {
      setError(err.message || 'Failed to load data')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleBorrow = async (formData) => {
    try {
      await borrowingApi.borrowBook(formData)
      setShowBorrowForm(false)
      await fetchAllData()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to record borrowing')
    }
  }

  const handleReturn = async (formData) => {
    try {
      await borrowingApi.returnBook(formData)
      setShowReturnForm(false)
      await fetchAllData()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to record return')
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Borrowing & Returns</h2>
        <div className="space-x-4">
          <button
            onClick={() => setShowBorrowForm(!showBorrowForm)}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition"
          >
            {showBorrowForm ? 'Cancel' : '+ Record Borrow'}
          </button>
          <button
            onClick={() => setShowReturnForm(!showReturnForm)}
            className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg transition"
          >
            {showReturnForm ? 'Cancel' : '+ Record Return'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
          <button
            onClick={() => setError(null)}
            className="float-right text-red-600 hover:text-red-800 font-bold"
          >
            ✕
          </button>
        </div>
      )}

      {showBorrowForm && (
        <BorrowForm
          availableBooks={books.filter(b => b.available)}
          members={members}
          onSubmit={handleBorrow}
        />
      )}

      {showReturnForm && (
        <ReturnForm
          activeBorrowings={activeBorrowings}
          onSubmit={handleReturn}
        />
      )}

      {loading ? (
        <div className="text-center py-10">Loading borrowing records...</div>
      ) : (
        <>
          <BorrowingTable
            title="Active Borrowings"
            borrowings={activeBorrowings}
            showStatus="active"
          />
          <BorrowingTable
            title="All Borrowing Records"
            borrowings={borrowings}
            showStatus="all"
          />
        </>
      )}
    </div>
  )
}
