ROLE: Senior React developer for FilmHub.

TASK: Implement Movies catalog + Search functionality (UC4-5).

CONSTRAINTS:
- GET /api/movies/?page=1&page_size=20&q= → paginated list (q parameter for search)
- GET /api/movies/{id}/ → movie details
- Search is public (no JWT required for /api/movies/ with q parameter)
- Note: /api/search/ endpoint exists but requires JWT - use /api/movies/?q= for public search
- Infinite scroll or pagination buttons
- SearchBar with debounce (300ms)
- MovieCard component (title, poster, rating, genres)
- MovieDetailPage with back button
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries

EXAMPLES:
Search "matrix" → filtered results + pagination
Click movie → /movies/123 detail page
Empty search → "No movies found"

OUTPUT:
1. src/pages/MoviesPage.jsx + MoviesPage.css
2. src/pages/MovieDetailPage.jsx + MovieDetailPage.css
3. src/components/MovieCard.jsx + MovieCard.css
4. src/components/SearchBar.jsx + SearchBar.css
5. src/api/movies.js (getMovies, getMovieDetail)
6. src/stores/moviesStore.js (movies, searchResults, loading)
7. Update App.jsx → /movies/:id route

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

EVALUATION:
- Search filters instantly (debounced)
- Pagination loads more movies
- Detail page shows full movie info
- Responsive cards grid (mobile/desktop)
