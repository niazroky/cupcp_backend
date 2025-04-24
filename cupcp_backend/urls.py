from django.contrib import admin
from django.urls import path, include

# ───────────────────────────────────────────────────────
# URL Configuration for the Backend
# ───────────────────────────────────────────────────────

urlpatterns = [
    # Django Admin Panel (For managing models, users, and permissions)
    path('admin/', admin.site.urls),

    # API Endpoints (Includes routes from the 'accounts' app)
    path('api/', include('accounts.urls')),

    # Student Manager: Exam Registration
    path("api/student-manager/", include("student_manager.urls")),
]
