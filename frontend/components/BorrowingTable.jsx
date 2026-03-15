'use client'

import DataTable from '@/components/DataTable'

export default function BorrowingTable({ title, borrowings, showStatus, loading, pagination }) {
  const filteredBorrowings =
    showStatus === 'active' ? borrowings.filter((b) => b.is_active) : borrowings

  const columns = [
    {
      key: 'id',
      label: 'Record ID',
      width: '5rem',
      render: (row) => <span className="font-mono bg-gray-50">#{row.id}</span>,
    },
    {
      key: 'book',
      label: 'Book',
      render: (row) => (
        <div>
          <div className="font-medium">{row.book?.title}</div>
          <div className="text-gray-600 text-xs">{row.book?.author}</div>
        </div>
      ),
    },
    { key: 'member', label: 'Member', render: (row) => row.member?.name },
    {
      key: 'borrowed_date',
      label: 'Borrowed',
      render: (row) => new Date(row.borrowed_date).toLocaleDateString(),
    },
    {
      key: 'returned_date',
      label: 'Returned',
      render: (row) =>
        row.returned_date ? new Date(row.returned_date).toLocaleDateString() : '—',
    },
    {
      key: 'is_active',
      label: 'Status',
      render: (row) => (
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            row.is_active ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
          }`}
        >
          {row.is_active ? 'Active' : 'Returned'}
        </span>
      ),
    },
  ]

  return (
    <DataTable
      title={title}
      columns={columns}
      data={filteredBorrowings}
      loading={loading}
      pagination={pagination}
      emptyMessage="No borrowing records found"
    />
  )
}
