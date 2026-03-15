'use client'

import { useState, useEffect, useCallback } from 'react'
import { bookApi } from '@/lib/api'
import BookForm from '@/components/BookForm'
import BookTable from '@/components/BookTable'

const PAGE_SIZE = 10

export default function BooksPage() {
  const [books, setBooks] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingBook, setEditingBook] = useState(null)

  const fetchBooks = useCallback(async (pageNum = page) => {
    try {
      setLoading(true)
      setError(null)
      const skip = (pageNum - 1) * PAGE_SIZE
      const response = await bookApi.getBooks({ skip, limit: PAGE_SIZE })
      const data = response.data?.items ?? response.data
      const totalCount = response.data?.total ?? (Array.isArray(data) ? data.length : 0)
      setBooks(Array.isArray(data) ? data : [])
      setTotal(totalCount)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load books')
      console.error('Error fetching books:', err)
    } finally {
      setLoading(false)
    }
  }, [page])

  useEffect(() => {
    fetchBooks(page)
  }, [page, fetchBooks])

  const handleAddBook = async (formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await bookApi.createBook(formData)
      setShowForm(false)
      await fetchBooks(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to create book')
    } finally {
      setSubmitting(false)
    }
  }

  const handleUpdateBook = async (bookId, formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await bookApi.updateBook(bookId, formData)
      setEditingBook(null)
      await fetchBooks(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to update book')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteBook = async (bookId) => {
    if (!confirm('Are you sure you want to delete this book?')) return
    try {
      setSubmitting(true)
      setError(null)
      await bookApi.deleteBook(bookId)
      await fetchBooks(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to delete book')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingBook(null)
  }

  const isBusy = loading || submitting

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Books Management</h2>
        <button
          type="button"
          onClick={() => setShowForm(true)}
          disabled={isBusy}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          + Add Book
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {(showForm || editingBook) && (
        <BookForm
          book={editingBook}
          onSubmit={editingBook ? (data) => handleUpdateBook(editingBook.id, data) : handleAddBook}
          onCancel={handleCancel}
          submitting={submitting}
        />
      )}

      <BookTable
        books={books}
        onEdit={(book) => setEditingBook(book)}
        onDelete={handleDeleteBook}
        loading={loading}
        actionsDisabled={submitting}
        pagination={
          total > PAGE_SIZE
            ? {
                page,
                pageSize: PAGE_SIZE,
                total,
                onPageChange: setPage,
              }
            : undefined
        }
      />
    </div>
  )
}
