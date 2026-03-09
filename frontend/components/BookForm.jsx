'use client'

import { useState, useEffect } from 'react'

export default function BookForm({ book, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({ title: '', author: '' })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (book) {
      setFormData({ title: book.title, author: book.author })
    }
  }, [book])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}
    if (!formData.title.trim()) newErrors.title = 'Title is required'
    if (!formData.author.trim()) newErrors.author = 'Author is required'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate()) {
      onSubmit(formData)
      setFormData({ title: '', author: '' })
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        {book ? 'Edit Book' : 'Add New Book'}
      </h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Book Title
          </label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.title ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., The Great Gatsby"
          />
          {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Author
          </label>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.author ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., F. Scott Fitzgerald"
          />
          {errors.author && <p className="text-red-500 text-sm mt-1">{errors.author}</p>}
        </div>

        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition font-medium"
          >
            {book ? 'Update' : 'Add'} Book
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-lg transition font-medium"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
