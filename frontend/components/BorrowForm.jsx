'use client'

import { useState } from 'react'

export default function BorrowForm({ availableBooks, members, onSubmit, submitting = false }) {
  const [formData, setFormData] = useState({ book_id: '', member_id: '' })
  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value ? parseInt(value) : '' }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}
    if (!formData.book_id) newErrors.book_id = 'Please select a book'
    if (!formData.member_id) newErrors.member_id = 'Please select a member'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate() && !submitting) {
      onSubmit(formData)
      setFormData({ book_id: '', member_id: '' })
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Record Book Borrowing</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Select Book
          </label>
          <select
            name="book_id"
            value={formData.book_id}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${
              errors.book_id ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">-- Choose a book --</option>
            {availableBooks.map(book => (
              <option key={book.id} value={book.id}>
                {book.title} by {book.author}
              </option>
            ))}
          </select>
          {errors.book_id && <p className="text-red-500 text-sm mt-1">{errors.book_id}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Select Member
          </label>
          <select
            name="member_id"
            value={formData.member_id}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 ${
              errors.member_id ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">-- Choose a member --</option>
            {members.map(member => (
              <option key={member.id} value={member.id}>
                {member.name}
              </option>
            ))}
          </select>
          {errors.member_id && <p className="text-red-500 text-sm mt-1">{errors.member_id}</p>}
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? 'Recording...' : 'Record Borrowing'}
        </button>
      </form>
    </div>
  )
}
