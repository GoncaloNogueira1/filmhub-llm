Implement basic health checks and logging for FilmHub Django + React.

**RELEVANT FILES:**

1. `filmhub-backend/authentication/views.py` (where to add health_check):
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import models
# ... other existing views
```

2. `filmhub-backend/filmhub/urls.py` (where to add route):
```python
from django.contrib import admin
from django.urls import path, include
from movies.views import search_movies
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/movies/', include('movies.urls')),
    path('api/movies/', include('ratings.urls')),
    path('api/search/', search_movies, name='search'),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/watchlist/', include('watchlist.urls')),
]
```

3. `filmhub-backend/filmhub/settings.py` (where to add LOGGING):
```python
# ... other Django configurations ...
# Add LOGGING config at the end of the file
```

4. `frontend/src/components/ErrorBoundary/index.jsx` (improve):
```javascript
import React from 'react';
import Layout from '../Layout';
import Button from '../ui/Button';
import './ErrorBoundary.css';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
  }
  // ... rest of the code
}
```

**TASKS:**

1. **Health Check Endpoint:**
   - Add `health_check` function in `authentication/views.py`:
     * Use `@api_view(['GET'])` and `@permission_classes([AllowAny])`
     * Import: `from django.http import JsonResponse`, `from django.db import connection`
     * Check DB: `connection.ensure_connection()` or `connection.cursor()`
     * Return JSON: `{"status": "healthy", "database": "connected", "timestamp": "2024-..."}`
     * If fails: `{"status": "unhealthy", "database": "disconnected"}`
   
   - Add to `filmhub/urls.py`:
     ```python
     from authentication.views import health_check
     # ... in urlpatterns:
     path('api/health/', health_check, name='health'),
     ```

2. **JSON Logging:**
   - In `settings.py`, add at the end:
     ```python
     LOGGING = {
         'version': 1,
         'disable_existing_loggers': False,
         'formatters': {
             'json': {
                 'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s"}',
                 'datefmt': '%Y-%m-%d %H:%M:%S'
             },
         },
         'handlers': {
             'console': {
                 'class': 'logging.StreamHandler',
                 'formatter': 'json',
             },
         },
         'loggers': {
             'django': {
                 'handlers': ['console'],
                 'level': 'INFO',
             },
             'authentication': {
                 'handlers': ['console'],
                 'level': 'ERROR',
             },
         },
     }
     ```

3. **ErrorBoundary:**
   - Improve `componentDidCatch` in `ErrorBoundary/index.jsx`:
     ```javascript
     componentDidCatch(error, errorInfo) {
       const errorLog = {
         timestamp: new Date().toISOString(),
         error: error.message,
         stack: errorInfo.componentStack,
         userAgent: navigator.userAgent
       };
       console.error('ErrorBoundary:', JSON.stringify(errorLog));
       this.setState({
         error,
         errorInfo
       });
     }
     ```

**EXPECTED OUTPUT:**
- Complete code for all 4 modified files
- Test: `curl http://localhost:8000/api/health/` should return valid JSON

Keep compatible with existing Django 4.2 + DRF and React.

