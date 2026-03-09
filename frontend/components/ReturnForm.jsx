'use client'

import { useState } from 'react'

export default function ReturnForm({ activeBorrowings, onSubmit }) {
  const [formData, setFormData] = useState({ borrowing_id: '' })
  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { value } = e.target
    setFormData({ borrowing_id: value ? parseInt(value) : '' })
    if (errors.borrowing_id) {
      setErrors({})
    }
  }

  const validate = () => {
    const newErrors = {}
    if (!formData.borrowing_id) newErrors.borrowing_id = 'Please select a borrowing record'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate()) {
      onSubmit(formData)
      setFormData({ borrowing_id: '' })
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Record Book Return</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Select Borrowing Record
          </label>
          <select
            value={formData.borrowing_id}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
              errors.borrowing_id ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">-- Choose a record --</option>
            {activeBorrowings.map(borrowing => {
              const daysOut = Math.floor(
                (new Date() - new Date(borrowing.borrowed_date)) / (1000 * 60 * 60 * 24)
              )
              return (
                <option key={borrowing.id} value={borrowing.id}>
                  {borrowing.book.title} - {borrowing.member.name} ({daysOut} days)
                </option>
              )
            })}
          </select>
          {errors.borrowing_id && <p className="text-red-500 text-sm mt-1">{errors.borrowing_id}</p>}
        </div>

        <button
          type="submit"
          className="w-full bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg transition font-medium"
        >
          Record Return
        </button>
      </form>
    </div>
  )
}
