export default function BorrowingTable({ title, borrowings, showStatus }) {
  const filteredBorrowings = showStatus === 'active' 
    ? borrowings.filter(b => b.is_active) 
    : borrowings

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      </div>
      <div className="overflow-x-auto">
        {filteredBorrowings.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No borrowing records found</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-100 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 w-20">Record ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Book</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Member</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Borrowed</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Returned</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredBorrowings.map((borrowing) => (
                <tr key={borrowing.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm font-mono text-gray-900 bg-gray-50">#{borrowing.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <div className="font-medium">{borrowing.book.title}</div>
                    <div className="text-gray-600 text-xs">{borrowing.book.author}</div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{borrowing.member.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {new Date(borrowing.borrowed_date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {borrowing.returned_date 
                      ? new Date(borrowing.returned_date).toLocaleDateString()
                      : '—'}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      borrowing.is_active
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {borrowing.is_active ? 'Active' : 'Returned'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
