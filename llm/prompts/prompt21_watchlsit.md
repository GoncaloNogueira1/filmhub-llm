ROLE: Senior React developer for FilmHub.

TASK: Implement WatchlistPage + watchlist actions (UC8-10).

CONSTRAINTS:
- GET /api/watchlist/ → user watchlist
- POST /api/watchlist/ → {movie_id}
- DELETE /api/watchlist/{movie_id}/
- JWT required
- Add/Remove buttons on MovieCard
- Watchlist badge counter in nav
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries

EXAMPLES:
MovieCard → "Add to watchlist" → POST → button changes to "Remove"
WatchlistPage → list with remove buttons
Empty → "Your watchlist is empty"

OUTPUT:
1. src/pages/WatchlistPage.jsx + WatchlistPage.css
2. src/components/WatchlistButton.jsx + WatchlistButton.css
3. src/api/watchlist.js (getWatchlist, addToWatchlist, removeFromWatchlist)
4. src/stores/watchlistStore.js
5. Update MovieCard.jsx → integrate WatchlistButton
6. Update App.jsx → /watchlist route (protected)

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

EVALUATION:
- Toggle buttons work (add → remove → add)
- Watchlist syncs instantly
- Badge counter updates
- Responsive layout works on mobile/desktop

