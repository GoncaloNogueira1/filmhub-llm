import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import ProtectedRoute from '../ProtectedRoute'

const mockUseAuthStore = vi.fn()

vi.mock('../stores/authStore', () => ({
  default: mockUseAuthStore
}))

describe('ProtectedRoute', () => {

  it('redirects to /login when not authenticated', () => {
    mockUseAuthStore.mockReturnValue({
      isAuthenticated: false,
      login: vi.fn(),
      logout: vi.fn(),
      user: null
    })
    
    render(
      <MemoryRouter initialEntries={['/protected']}>
        <ProtectedRoute>
          <div data-testid="protected-content">Protected Content</div>
        </ProtectedRoute>
      </MemoryRouter>
    )
    
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument()
  })
})

