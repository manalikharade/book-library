'use client'

import DataTable from '@/components/DataTable'

const columns = [
  { key: 'id', label: 'Member ID', width: '6rem', render: (row) => <span className="font-mono bg-gray-50">#{row.id}</span> },
  { key: 'name', label: 'Name' },
  { key: 'contact_no', label: 'Contact' },
  { key: 'address', label: 'Address' },
]

export default function MemberTable({ members, onEdit, onDelete, loading, actionsDisabled, pagination }) {
  return (
    <DataTable
      columns={columns}
      data={members}
      loading={loading}
      pagination={pagination}
      emptyMessage="No members found"
      renderActions={(row, disabled) => (
        <>
          <button
            type="button"
            onClick={() => onEdit(row)}
            disabled={disabled}
            className="text-blue-600 hover:text-blue-800 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Edit
          </button>
          <button
            type="button"
            onClick={() => onDelete(row.id)}
            disabled={disabled}
            className="text-red-600 hover:text-red-800 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Delete
          </button>
        </>
      )}
      actionsDisabled={actionsDisabled}
    />
  )
}
