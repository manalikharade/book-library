export default function MemberTable({ members, onEdit, onDelete }) {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="overflow-x-auto">
        {members.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No members found</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-100 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700 w-24">Member ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Name</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Contact</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Address</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {members.map((member) => (
                <tr key={member.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm font-mono text-gray-900 bg-gray-50">#{member.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{member.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{member.contact_no}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{member.address}</td>
                  <td className="px-6 py-4 text-sm space-x-2">
                    <button
                      onClick={() => onEdit(member)}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => onDelete(member.id)}
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
