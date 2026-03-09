'use client'

import { useState, useEffect } from 'react'

export default function MemberForm({ member, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    contact_no: '',
    address: '',
  })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (member) {
      setFormData({
        name: member.name,
        contact_no: member.contact_no,
        address: member.address,
      })
    }
  }, [member])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}
    if (!formData.name.trim()) newErrors.name = 'Name is required'
    if (!formData.contact_no.trim()) newErrors.contact_no = 'Contact number is required'
    if (!formData.address.trim()) newErrors.address = 'Address is required'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate()) {
      onSubmit(formData)
      setFormData({ name: '', contact_no: '', address: '' })
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        {member ? 'Edit Member' : 'Add New Member'}
      </h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Name
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., John Smith"
          />
          {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Contact Number
          </label>
          <input
            type="text"
            name="contact_no"
            value={formData.contact_no}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.contact_no ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., +1-234-567-8901"
          />
          {errors.contact_no && <p className="text-red-500 text-sm mt-1">{errors.contact_no}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Address
          </label>
          <textarea
            name="address"
            value={formData.address}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.address ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., 123 Main St, Springfield, IL"
            rows="3"
          />
          {errors.address && <p className="text-red-500 text-sm mt-1">{errors.address}</p>}
        </div>

        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition font-medium"
          >
            {member ? 'Update' : 'Add'} Member
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
