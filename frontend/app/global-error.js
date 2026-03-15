'use client'

/**
 * Next.js App Router: global-error.js catches errors in the root layout.
 * Renders a full-page fallback (must include html/body for root).
 */
export default function GlobalError({ error, reset }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, sans-serif', background: '#fef2f2', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ maxWidth: 420, padding: 24, textAlign: 'center' }}>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#991b1b', marginBottom: 8 }}>
            Application error
          </h1>
          <p style={{ color: '#b91c1c', fontSize: 14, marginBottom: 24 }}>
            {error?.message || 'An unexpected error occurred.'}
          </p>
          <button
            type="button"
            onClick={reset}
            style={{
              padding: '10px 20px',
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              borderRadius: 8,
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            Try again
          </button>
        </div>
      </body>
    </html>
  )
}
