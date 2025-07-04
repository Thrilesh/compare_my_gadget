from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import gadget_detail

urlpatterns = [
    path('', views.user_login, name='login'),  # Changed this line
    path('home/', views.home, name='home'),    # Added new path for home
    path('compare/', views.compare_gadgets, name='compare_gadgets'),
    path('reviews/', views.reviews, name='reviews'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('account/', views.account, name='account'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('gadget/<int:gadget_id>/', gadget_detail, name='gadget_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
