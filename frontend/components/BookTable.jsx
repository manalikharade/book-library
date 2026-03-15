'use client'

import DataTable from '@/components/DataTable'

const columns = [
  { key: 'id', label: 'Book Code', width: '6rem', render: (row) => <span className="font-mono bg-gray-50">#{row.id}</span> },
  { key: 'title', label: 'Title' },
  { key: 'author', label: 'Author' },
  {
    key: 'available',
    label: 'Status',
    render: (row) => (
      <span
        className={`px-3 py-1 rounded-full text-xs font-semibold ${
          row.available ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
        }`}
      >
        {row.available ? 'Available' : 'Borrowed'}
      </span>
    ),
  },
]

export default function BookTable({ books, onEdit, onDelete, loading, actionsDisabled, pagination }) {
  return (
    <DataTable
      columns={columns}
      data={books}
      loading={loading}
      pagination={pagination}
      emptyMessage="No books found"
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
