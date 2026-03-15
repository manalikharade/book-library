'use client'

import { useState, useEffect, useCallback } from 'react'
import { borrowingApi, bookApi, memberApi } from '@/lib/api'
import BorrowForm from '@/components/BorrowForm'
import ReturnForm from '@/components/ReturnForm'
import BorrowingTable from '@/components/BorrowingTable'

const PAGE_SIZE = 10

export default function BorrowingPage() {
  const [borrowings, setBorrowings] = useState([])
  const [borrowingsTotal, setBorrowingsTotal] = useState(0)
  const [borrowingsPage, setBorrowingsPage] = useState(1)
  const [activeBorrowings, setActiveBorrowings] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [showBorrowForm, setShowBorrowForm] = useState(false)
  const [showReturnForm, setShowReturnForm] = useState(false)
  const [books, setBooks] = useState([])
  const [members, setMembers] = useState([])

  const fetchAllData = useCallback(async () => {
    setError(null)
    const [booksRes, membersRes, activeRes] = await Promise.all([
      bookApi.getBooks({ skip: 0, limit: 10000 }),
      memberApi.getMembers({ skip: 0, limit: 10000 }),
      borrowingApi.getActiveBorrowings(),
    ])
    setBooks(booksRes.data?.items ?? booksRes.data ?? [])
    setMembers(membersRes.data?.items ?? membersRes.data ?? [])
    setActiveBorrowings(activeRes.data ?? [])
  }, [])

  const fetchBorrowingsPage = useCallback(async (pageNum) => {
    setError(null)
    const skip = (pageNum - 1) * PAGE_SIZE
    const response = await borrowingApi.getBorrowings({ skip, limit: PAGE_SIZE })
    const data = response.data?.items ?? response.data
    const total = response.data?.total ?? (Array.isArray(data) ? data.length : 0)
    setBorrowings(Array.isArray(data) ? data : [])
    setBorrowingsTotal(total)
  }, [])

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      setLoading(true)
      try {
        await Promise.all([fetchAllData(), fetchBorrowingsPage(1)])
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Failed to load data')
          console.error('Error:', err)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    if (borrowingsPage === 1) return
    let cancelled = false
    const load = async () => {
      setLoading(true)
      try {
        await fetchBorrowingsPage(borrowingsPage)
      } catch (err) {
        if (!cancelled) setError(err.message || 'Failed to load borrowings')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [borrowingsPage])

  const handleBorrow = async (formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await borrowingApi.borrowBook(formData)
      setShowBorrowForm(false)
      await fetchAllData()
      await fetchBorrowingsPage(borrowingsPage)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to record borrowing')
    } finally {
      setSubmitting(false)
    }
  }

  const handleReturn = async (formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await borrowingApi.returnBook(formData)
      setShowReturnForm(false)
      await fetchAllData()
      await fetchBorrowingsPage(borrowingsPage)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to record return')
    } finally {
      setSubmitting(false)
    }
  }

  const isBusy = loading || submitting

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Borrowing & Returns</h2>
        <div className="space-x-4">
          <button
            type="button"
            onClick={() => setShowBorrowForm(!showBorrowForm)}
            disabled={isBusy}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {showBorrowForm ? 'Cancel' : '+ Record Borrow'}
          </button>
          <button
            type="button"
            onClick={() => setShowReturnForm(!showReturnForm)}
            disabled={isBusy}
            className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {showReturnForm ? 'Cancel' : '+ Record Return'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
          <button
            type="button"
            onClick={() => setError(null)}
            className="float-right text-red-600 hover:text-red-800 font-bold"
          >
            ✕
          </button>
        </div>
      )}

      {showBorrowForm && (
        <BorrowForm
          availableBooks={books.filter((b) => b.available)}
          members={members}
          onSubmit={handleBorrow}
          submitting={submitting}
        />
      )}

      {showReturnForm && (
        <ReturnForm
          activeBorrowings={activeBorrowings}
          onSubmit={handleReturn}
          submitting={submitting}
        />
      )}

      <BorrowingTable
        title="Active Borrowings"
        borrowings={activeBorrowings}
        showStatus="active"
        loading={loading}
      />
      <BorrowingTable
        title="All Borrowing Records"
        borrowings={borrowings}
        showStatus="all"
        loading={loading}
        pagination={
          borrowingsTotal > PAGE_SIZE
            ? {
                page: borrowingsPage,
                pageSize: PAGE_SIZE,
                total: borrowingsTotal,
                onPageChange: setBorrowingsPage,
              }
            : undefined
        }
      />
    </div>
  )
}
