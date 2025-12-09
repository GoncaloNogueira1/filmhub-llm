import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import LoginPage from '../LoginPage'

// Mock authAPI (default export)
const mockAuthAPI = {
  login: vi.fn(),
  register: vi.fn()
}

vi.mock('../../api/auth', () => ({
  default: {
    login: vi.fn(),
    register: vi.fn()
  }
}))

// Mock useAuthStore (default export, Zustand hook)
vi.mock('../../stores/authStore', () => ({
  default: vi.fn()
}))

// Mock React Router
const mockNavigate = vi.fn()

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

// Mock Navbar to avoid complex dependencies
vi.mock('../../components/Navbar', () => ({
  default: () => <nav data-testid="navbar">Navbar</nav>
}))

describe('LoginPage', () => {
  beforeEach(async () => {
    vi.clearAllMocks()
    const authModule = await import('../../api/auth')
    const authStoreModule = await import('../../stores/authStore')
    authModule.default.login.mockResolvedValue({ user: {}, tokens: { access: 'token', refresh: 'refresh' } })
    authStoreModule.default.mockReturnValue({
      isAuthenticated: false,
      login: vi.fn(),
      logout: vi.fn(),
      user: null
    })
  })

  it('renders login form', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )
    
    expect(screen.getByPlaceholderText(/email@example.com/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/••••••••/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })


})

