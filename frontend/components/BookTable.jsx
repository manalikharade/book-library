export default function BookTable({ books, onEdit, onDelete }) {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="overflow-x-auto">
        {books.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No books found</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-100 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 w-24">Book Code</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Title</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Author</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {books.map((book) => (
                <tr key={book.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm font-mono text-gray-900 bg-gray-50">#{book.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{book.title}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{book.author}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      book.available 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {book.available ? 'Available' : 'Borrowed'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm space-x-2">
                    <button
                      onClick={() => onEdit(book)}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => onDelete(book.id)}
                      className="text-red-600 hover:text-red-800 font-medium"
                    >
                      Delete
                    </button>
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
