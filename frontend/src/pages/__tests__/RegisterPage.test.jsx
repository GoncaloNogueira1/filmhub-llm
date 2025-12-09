import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import RegisterPage from '../RegisterPage'

vi.mock('../../api/auth', () => ({
  default: {
    login: vi.fn(),
    register: vi.fn()
  }
}))

const mockNavigate = vi.fn()

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

describe('RegisterPage', () => {
  beforeEach(async () => {
    vi.clearAllMocks()
    const authModule = await import('../../api/auth')
    authModule.default.register.mockResolvedValue({ user: {} })
  })

  it('renders register form', () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    )
    
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument()
  })

  it('shows password mismatch error', async () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    )
    
    await userEvent.type(screen.getByLabelText(/^password$/i), 'password123')
    await userEvent.type(screen.getByLabelText(/confirm password/i), 'different')
    await userEvent.click(screen.getByRole('button', { name: /create account/i }))
    
    await waitFor(() => {
      expect(screen.getByText(/passwords do not match/i)).toBeInTheDocument()
    })
  })

  it('calls authAPI.register on form submit', async () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    )
    
    await userEvent.type(screen.getByLabelText(/email address/i), 'new@example.com')
    await userEvent.type(screen.getByLabelText(/^password$/i), 'password123')
    await userEvent.type(screen.getByLabelText(/confirm password/i), 'password123')
    await userEvent.click(screen.getByRole('button', { name: /create account/i }))
    
    await waitFor(async () => {
      const authModule = await import('../../api/auth')
      expect(authModule.default.register).toHaveBeenCalled()
    }, { timeout: 2000 })
  })

  it('shows password strength validation error', async () => {
    render(
      <BrowserRouter>
        <RegisterPage />
      </BrowserRouter>
    )
    
    await userEvent.type(screen.getByLabelText(/^password$/i), 'weak')
    await userEvent.click(screen.getByRole('button', { name: /create account/i }))
    
    await waitFor(() => {
      expect(screen.getByText(/password must be at least 8 characters/i)).toBeInTheDocument()
    })
  })
})

