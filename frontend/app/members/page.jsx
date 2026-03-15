'use client'

import { useState, useEffect, useCallback } from 'react'
import { memberApi } from '@/lib/api'
import MemberForm from '@/components/MemberForm'
import MemberTable from '@/components/MemberTable'

const PAGE_SIZE = 10

export default function MembersPage() {
  const [members, setMembers] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingMember, setEditingMember] = useState(null)

  const fetchMembers = useCallback(async (pageNum = page) => {
    try {
      setLoading(true)
      setError(null)
      const skip = (pageNum - 1) * PAGE_SIZE
      const response = await memberApi.getMembers({ skip, limit: PAGE_SIZE })
      const data = response.data?.items ?? response.data
      const totalCount = response.data?.total ?? (Array.isArray(data) ? data.length : 0)
      setMembers(Array.isArray(data) ? data : [])
      setTotal(totalCount)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load members')
      console.error('Error fetching members:', err)
    } finally {
      setLoading(false)
    }
  }, [page])

  useEffect(() => {
    fetchMembers(page)
  }, [page, fetchMembers])

  const handleAddMember = async (formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await memberApi.createMember(formData)
      setShowForm(false)
      await fetchMembers(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to create member')
    } finally {
      setSubmitting(false)
    }
  }

  const handleUpdateMember = async (memberId, formData) => {
    try {
      setSubmitting(true)
      setError(null)
      await memberApi.updateMember(memberId, formData)
      setEditingMember(null)
      await fetchMembers(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to update member')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteMember = async (memberId) => {
    if (!confirm('Are you sure you want to delete this member?')) return
    try {
      setSubmitting(true)
      setError(null)
      await memberApi.deleteMember(memberId)
      await fetchMembers(page)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to delete member')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingMember(null)
  }

  const isBusy = loading || submitting

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Members Management</h2>
        <button
          type="button"
          onClick={() => setShowForm(true)}
          disabled={isBusy}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
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
          onSubmit={
            editingMember ? (data) => handleUpdateMember(editingMember.id, data) : handleAddMember
          }
          onCancel={handleCancel}
          submitting={submitting}
        />
      )}

      <MemberTable
        members={members}
        onEdit={(member) => setEditingMember(member)}
        onDelete={handleDeleteMember}
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
