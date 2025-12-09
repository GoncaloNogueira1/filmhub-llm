ROLE: React testing specialist with Vitest and React Testing Library.

TASK: Set up Vitest for FilmHub frontend and create tests for key components.

CONSTRAINTS:
- Stack: React 19, Vite, Zustand, React Router DOM v7
- Vitest in package.json scripts but not installed
- Use @testing-library/react, @testing-library/jest-dom, @testing-library/user-event
- Use main .jsx files (LoginPage.jsx, not LoginPage/index.jsx)
- Use relative imports (../api/auth, ../stores/authStore), NOT alias paths like @/

IMPORTANT - ACTUAL CODE STRUCTURE:
- API: `authAPI` is default export from `../api/auth` (has login, register methods)
- Store: `useAuthStore` is default export from `../stores/authStore` (Zustand hook)
- Components import: `import authAPI from '../api/auth'` and `import useAuthStore from '../stores/authStore'`
- LoginPage calls: `await authAPI.login(formData)` then `navigate('/movies')`
- useAuthStore returns: `{ isAuthenticated, login, logout, user }` object

MOCKING REQUIREMENTS:
- Mock `../api/auth` as default export with login/register methods
- Mock `../stores/authStore` as default export (Zustand hook) returning object
- Mock `react-router-dom` useNavigate hook
- Use vi.mock() with proper module paths

WHAT TO TEST:

LoginPage: form renders, validation errors, calls authAPI.login(), navigates on success, redirects if authenticated
RegisterPage: form renders, password validation, calls authAPI.register(), navigates on success
MovieCard: renders movie data, poster fallback, click navigation, WatchlistButton integration
ProtectedRoute: renders children if authenticated, redirects to /login if not
Navbar: shows correct links based on auth state, logout functionality, watchlist badge

OUTPUT:
- `frontend/package.json`: Add vitest, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, jsdom to devDependencies
- `frontend/vitest.config.js`: Configure for React with jsdom environment, setupFiles
- `frontend/src/test/setup.js`: Import @testing-library/jest-dom
- Test files in __tests__ folders:
  - `frontend/src/pages/__tests__/LoginPage.test.jsx` (5+ tests)
  - `frontend/src/pages/__tests__/RegisterPage.test.jsx` (4+ tests)
  - `frontend/src/components/__tests__/MovieCard.test.jsx` (4+ tests)
  - `frontend/src/components/__tests__/ProtectedRoute.test.jsx` (2+ tests)
  - `frontend/src/components/__tests__/Navbar.test.jsx` (4+ tests)

MOCK EXAMPLES (use these patterns):
```javascript
// Mock authAPI (default export)
vi.mock('../api/auth', () => ({
  default: {
    login: vi.fn().mockResolvedValue({ user: {}, tokens: { access: 'token', refresh: 'refresh' } }),
    register: vi.fn().mockResolvedValue({ user: {} })
  }
}))

// Mock useAuthStore (default export, Zustand hook)
vi.mock('../stores/authStore', () => ({
  default: () => ({
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    user: null
  })
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
```

EVALUATION:
- `npm test` runs successfully
- All tests pass (19+ total)
- Mocks use correct import paths (relative, not alias)
- authAPI mocked as default export
- useAuthStore mocked as default export hook
- Tests work in CI
