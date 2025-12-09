import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import MovieCard from '../MovieCard'

// Mock WatchlistButton
vi.mock('../WatchlistButton', () => ({
  default: ({ movieId }) => (
    <button data-testid="watchlist-btn">Watchlist {movieId}</button>
  )
}))

describe('MovieCard', () => {
  const mockMovie = {
    id: 1,
    title: 'Test Movie',
    poster_path: '/test-poster.jpg',
    overview: 'Movie description',
    vote_average: 8.5,
    release_year: 2023
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders movie data correctly', () => {
    render(
      <BrowserRouter>
        <MovieCard movie={mockMovie} />
      </BrowserRouter>
    )
    
    expect(screen.getByText('Test Movie')).toBeInTheDocument()
    expect(screen.getByText('2023')).toBeInTheDocument()
  })

  it('has correct Link to movie page', () => {
    render(
      <BrowserRouter>
        <MovieCard movie={mockMovie} />
      </BrowserRouter>
    )
    
    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', '/movies/1')
  })


  it('renders WatchlistButton integration', () => {
    render(
      <BrowserRouter>
        <MovieCard movie={mockMovie} />
      </BrowserRouter>
    )
    
    expect(screen.getByTestId('watchlist-btn')).toBeInTheDocument()
  })
})

