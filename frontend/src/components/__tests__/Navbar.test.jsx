import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import Navbar from '../Navbar'

const mockUseAuthStore = vi.fn()
vi.mock('../stores/authStore', () => ({
  default: mockUseAuthStore
}))

const mockUseWatchlistStore = vi.fn()
vi.mock('../stores/watchlistStore', () => ({
  default: mockUseWatchlistStore
}))

// Mock authAPI for logout
const mockAuthAPI = {
  logout: vi.fn()
}
vi.mock('../api/auth', () => ({
  default: mockAuthAPI
}))

describe('Navbar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockUseAuthStore.mockReturnValue({
      isAuthenticated: false,
      login: vi.fn(),
      logout: vi.fn(),
      user: null
    })
    mockUseWatchlistStore.mockReturnValue({ 
      count: 3,
      fetchWatchlist: vi.fn()
    })
  })

  it('shows login/register links when not authenticated', () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    )
    
    // Buttons are inside Links, so find by text content
    expect(screen.getByText(/login/i)).toBeInTheDocument()
    expect(screen.getByText(/sign up/i)).toBeInTheDocument()
    expect(screen.queryByText(/logout/i)).not.toBeInTheDocument()
  })

})

