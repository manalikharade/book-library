'use client'

import { useState, useEffect } from 'react'
import { memberApi } from '@/lib/api'
import MemberForm from '@/components/MemberForm'
import MemberTable from '@/components/MemberTable'

export default function MembersPage() {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingMember, setEditingMember] = useState(null)

  useEffect(() => {
    fetchMembers()
  }, [])

  const fetchMembers = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await memberApi.getAllMembers()
      setMembers(response.data)
    } catch (err) {
      setError(err.message || 'Failed to load members')
      console.error('Error fetching members:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddMember = async (formData) => {
    try {
      await memberApi.createMember(formData)
      setShowForm(false)
      await fetchMembers()
    } catch (err) {
      setError(err.message || 'Failed to create member')
    }
  }

  const handleUpdateMember = async (memberId, formData) => {
    try {
      await memberApi.updateMember(memberId, formData)
      setEditingMember(null)
      await fetchMembers()
    } catch (err) {
      setError(err.message || 'Failed to update member')
    }
  }

  const handleDeleteMember = async (memberId) => {
    if (confirm('Are you sure you want to delete this member?')) {
      try {
        await memberApi.deleteMember(memberId)
        await fetchMembers()
      } catch (err) {
        setError(err.message || 'Failed to delete member')
      }
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingMember(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Members Management</h2>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
        >
          + Add Member
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {(showForm || editingMember) && (
        <MemberForm
          member={editingMember}
          onSubmit={editingMember ? 
            (data) => handleUpdateMember(editingMember.id, data) : 
            handleAddMember
          }
          onCancel={handleCancel}
        />
      )}

      {loading ? (
        <div className="text-center py-10">Loading members...</div>
      ) : (
        <MemberTable
          members={members}
          onEdit={(member) => setEditingMember(member)}
          onDelete={handleDeleteMember}
        />
      )}
    </div>
  )
}
