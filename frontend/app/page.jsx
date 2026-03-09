'use client'

import { useState, useEffect } from 'react'
import { borrowingApi, bookApi, memberApi } from '@/lib/api'

export default function DashboardPage() {
  const [activeBorrowings, setActiveBorrowings] = useState([])
  const [stats, setStats] = useState({
    totalBooks: 0,
    availableBooks: 0,
    totalMembers: 0,
    activeBorrowings: 0,
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [borrowingsRes, booksRes, availableRes, membersRes] = await Promise.all([
        borrowingApi.getActiveBorrowings(),
        bookApi.getAllBooks(),
        bookApi.getAvailableBooks(),
        memberApi.getAllMembers(),
      ])

      setActiveBorrowings(borrowingsRes.data)
      setStats({
        totalBooks: booksRes.data.length,
        availableBooks: availableRes.data.length,
        totalMembers: membersRes.data.length,
        activeBorrowings: borrowingsRes.data.length,
      })
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data')
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ title, value, bgColor }) => (
    <div className={`${bgColor} text-white p-6 rounded-lg shadow`}>
      <p className="text-gray-100 text-sm font-semibold">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  )

  if (loading) return <div className="text-center py-10">Loading...</div>

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-gray-800">Dashboard</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="Total Books" value={stats.totalBooks} bgColor="bg-blue-500" />
        <StatCard title="Available Books" value={stats.availableBooks} bgColor="bg-green-500" />
        <StatCard title="Total Members" value={stats.totalMembers} bgColor="bg-purple-500" />
        <StatCard title="Active Borrowings" value={stats.activeBorrowings} bgColor="bg-orange-500" />
      </div>

      {/* Active Borrowings Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-xl font-bold text-gray-800">Currently Borrowed Books</h3>
        </div>
        <div className="overflow-x-auto">
          {activeBorrowings.length === 0 ? (
            <div className="p-6 text-center text-gray-500">No active borrowings</div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Book Title</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Author</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Member</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Borrowed Date</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Due Date</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Days Out</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Fine</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {activeBorrowings.map((borrowing) => {
                  const daysOut = Math.floor(
                    (new Date() - new Date(borrowing.borrowed_date)) / (1000 * 60 * 60 * 24)
                  )
                  const dueDate = new Date(borrowing.due_date)
                  const isOverdue = dueDate < new Date()
                  return (
                    <tr key={borrowing.id} className={isOverdue ? "bg-red-50 hover:bg-red-100" : "hover:bg-gray-50"}>
                      <td className="px-6 py-4 text-sm text-gray-900">{borrowing.book.title}</td>
                      <td className="px-6 py-4 text-sm text-gray-600">{borrowing.book.author}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">{borrowing.member.name}</td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {new Date(borrowing.borrowed_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className={`px-3 py-1 rounded text-xs font-semibold ${
                          isOverdue ? 'bg-red-200 text-red-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {dueDate.toLocaleDateString()}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          daysOut > 14 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                        }`}>
                          {daysOut} days
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm font-semibold">
                        <span className={borrowing.fine > 0 ? 'text-red-600' : 'text-gray-600'}>
                          {borrowing.fine === 0 ? '-' : `Rs.${borrowing.fine.toFixed(2)}`}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
