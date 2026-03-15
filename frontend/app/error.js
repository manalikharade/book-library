'use client'

import ErrorBoundary from '@/components/ErrorBoundary'

/**
 * Next.js App Router: error.js catches errors in the segment and below.
 * Renders this UI and allows recovery without full app crash.
 */
export default function Error({ error, reset }) {
  return (
    <div className="min-h-[300px] flex flex-col items-center justify-center p-8">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg border border-gray-200 p-8 text-center">
        <h2 className="text-xl font-bold text-gray-800 mb-2">Something went wrong</h2>
        <p className="text-gray-600 text-sm mb-6">
          {error?.message || 'An unexpected error occurred. Please try again.'}
        </p>
        <button
          type="button"
          onClick={reset}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition font-medium"
        >
          Try again
        </button>
      </div>
    </div>
  )
}
