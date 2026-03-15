'use client'

/**
 * Reusable DataTable with optional server-side pagination.
 * @param {Object} props
 * @param {Array<{ key: string, label: string, render?: (row) => ReactNode }>} props.columns
 * @param {Array} props.data
 * @param {boolean} [props.loading]
 * @param {{ page: number, pageSize: number, total: number, onPageChange: (page: number) => void }} [props.pagination]
 * @param {(row: any) => ReactNode} [props.renderActions]
 * @param {string} [props.emptyMessage]
 * @param {string} [props.title]
 */
export default function DataTable({
  columns,
  data = [],
  loading = false,
  pagination,
  renderActions,
  emptyMessage = 'No records found',
  title,
  actionsDisabled = false,
}) {
  const total = pagination?.total ?? data.length
  const page = pagination?.page ?? 1
  const pageSize = pagination?.pageSize ?? 10
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const hasPagination = pagination && total > pageSize

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {title && (
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-xl font-bold text-gray-800">{title}</h3>
        </div>
      )}
      <div className="overflow-x-auto">
        {loading ? (
          <div className="p-10 text-center text-gray-500">Loading...</div>
        ) : data.length === 0 ? (
          <div className="p-6 text-center text-gray-500">{emptyMessage}</div>
        ) : (
          <>
            <table className="w-full">
              <thead className="bg-gray-100 border-b border-gray-200">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.key}
                      className="px-6 py-3 text-left text-sm font-semibold text-gray-700"
                      style={col.width ? { width: col.width } : undefined}
                    >
                      {col.label}
                    </th>
                  ))}
                  {renderActions && (
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {data.map((row, idx) => (
                  <tr key={row.id ?? idx} className="hover:bg-gray-50 transition">
                    {columns.map((col) => (
                      <td key={col.key} className="px-6 py-4 text-sm text-gray-900">
                        {col.render ? col.render(row) : row[col.key]}
                      </td>
                    ))}
                    {renderActions && (
                      <td className="px-6 py-4 text-sm space-x-2">
                        {renderActions(row, actionsDisabled)}
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
            {hasPagination && (
              <div className="flex items-center justify-between px-6 py-3 border-t border-gray-200 bg-gray-50">
                <p className="text-sm text-gray-600">
                  Showing {(page - 1) * pageSize + 1}–{Math.min(page * pageSize, total)} of {total}
                </p>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => pagination.onPageChange(page - 1)}
                    disabled={page <= 1}
                    className="px-3 py-1 rounded border border-gray-300 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                  >
                    Previous
                  </button>
                  <span className="px-3 py-1 text-sm text-gray-700">
                    Page {page} of {totalPages}
                  </span>
                  <button
                    type="button"
                    onClick={() => pagination.onPageChange(page + 1)}
                    disabled={page >= totalPages}
                    className="px-3 py-1 rounded border border-gray-300 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
