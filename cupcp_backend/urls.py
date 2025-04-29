from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# ───────────────────────────────────────────────────────
# URL Configuration for the Backend
# ───────────────────────────────────────────────────────

def home(request):  # 👈 Add this
    return HttpResponse("<h1>Congrats, Your server is Running<h1>")

urlpatterns = [
    # Empty route - homepage
    path('', home),  # 👈 Empty path
    # Django Admin Panel (For managing models, users, and permissions)
    path('admin/', admin.site.urls),

    # API Endpoints (Includes routes from the 'accounts' app)
    path('api/', include('accounts.urls')),

    # Student Manager: Exam Registration
    path("api/student-manager/", include("student_manager.urls")),
]
