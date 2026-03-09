'use client'

import { useState, useEffect } from 'react'
import { bookApi } from '@/lib/api'
import BookForm from '@/components/BookForm'
import BookTable from '@/components/BookTable'

export default function BooksPage() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingBook, setEditingBook] = useState(null)

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await bookApi.getAllBooks()
      setBooks(response.data)
    } catch (err) {
      setError(err.message || 'Failed to load books')
      console.error('Error fetching books:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddBook = async (formData) => {
    try {
      await bookApi.createBook(formData)
      setShowForm(false)
      await fetchBooks()
    } catch (err) {
      setError(err.message || 'Failed to create book')
    }
  }

  const handleUpdateBook = async (bookId, formData) => {
    try {
      await bookApi.updateBook(bookId, formData)
      setEditingBook(null)
      await fetchBooks()
    } catch (err) {
      setError(err.message || 'Failed to update book')
    }
  }

  const handleDeleteBook = async (bookId) => {
    if (confirm('Are you sure you want to delete this book?')) {
      try {
        await bookApi.deleteBook(bookId)
        await fetchBooks()
      } catch (err) {
        setError(err.message || 'Failed to delete book')
      }
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingBook(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Books Management</h2>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
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
          onSubmit={editingBook ? 
            (data) => handleUpdateBook(editingBook.id, data) : 
            handleAddBook
          }
          onCancel={handleCancel}
        />
      )}

      {loading ? (
        <div className="text-center py-10">Loading books...</div>
      ) : (
        <BookTable
          books={books}
          onEdit={(book) => setEditingBook(book)}
          onDelete={handleDeleteBook}
        />
      )}
    </div>
  )
}
