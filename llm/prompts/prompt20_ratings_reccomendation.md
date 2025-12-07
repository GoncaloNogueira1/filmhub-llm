ROLE: Senior React developer for FilmHub.

TASK: Implement RatingForm + RecommendationsPage (UC6-7).

CONSTRAINTS:
- POST /api/movies/{id}/rate/ → {score: 1-5, comment?}
- GET /api/recommendations → personalized list
- JWT required (protected)
- Rating stars (1-5 clickable)
- Recommendations show predicted_score
- **CSS SEPARADO**: Use CSS files, NOT Tailwind classes in className
- Responsive design with CSS media queries

REASONING STEPS:
1. MovieDetailPage → show RatingForm with current user rating (if exists)
2. RatingForm → POST on submit → refresh movie detail + recommendations
3. RecommendationsPage → GET /api/recommendations → show top 20
4. Cold-start → show "Rate some movies to get recommendations"
5. Add "Rate this movie" buttons on recommendations

OUTPUT:
1. src/components/RatingForm.jsx + RatingForm.css
2. src/pages/RecommendationsPage.jsx + RecommendationsPage.css
3. Update MovieDetailPage.jsx → integrate RatingForm
4. src/api/ratings.js (rateMovie)
5. Update moviesStore.js → add user ratings
6. Update App.jsx → /recommendations route (protected)

**IMPORTANT**: All styling in separate .css files. NO Tailwind classes in className attributes.

EVALUATION:
- Rating stars clickable and submit
- Rating updates instantly in UI
- Recommendations refresh after rating
- Protected routes work
