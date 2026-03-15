'use client'

import { Component } from 'react'

/**
 * Reusable client-side error boundary. Catches JavaScript errors in child tree
 * and displays a fallback UI instead of crashing.
 */
export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      const { fallback, onRetry } = this.props
      if (typeof fallback === 'function') {
        return fallback({ error: this.state.error, reset: () => this.setState({ hasError: false, error: null }) })
      }
      if (fallback) return fallback
      return (
        <div className="min-h-[200px] flex flex-col items-center justify-center p-6 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="text-lg font-semibold text-red-800 mb-2">Something went wrong</h3>
          <p className="text-red-700 text-sm mb-4 text-center max-w-md">
            {this.state.error?.message || 'An unexpected error occurred.'}
          </p>
          {onRetry && (
            <button
              type="button"
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
            >
              Try again
            </button>
          )}
        </div>
      )
    }
    return this.props.children
  }
}
