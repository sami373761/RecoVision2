from django.urls import path
from .views import change_password
from .views import reset_user_saves
from . import views
urlpatterns = [
    path('films', views.films, name='films'),
    
    # Movies
    path('home', views.index, name='index'),
    path('film/<slug:slug>', views.film, name='film'),
    path('actors/<slug:slug>', views.actor, name='actor'),
    path('director/<slug:slug>', views.director, name='director'),
    path('kaydet/<int:movie_id>/', views.kaydet, name='kaydet'),
    path('kayitlar', views.kayitlar, name='kayitlar'),
    path('kategori', views.category, name='director'),
    
    # Books
    path('kitap/<slug:slug>', views.kitap, name='kitap'),
    path('yazar/<slug:slug>', views.yazar, name='yazar'),
    path('kaydet_kitap/<int:book_id>/', views.kaydet_kitap, name='kaydet_kitap'),
    path('kayitlar_kitap', views.kayitlar_kitap, name='kayitlar_kitap'),
    path('books', views.books, name='books'),
    
    # Series
    path('series', views.series, name='series'),
    path('serie/<slug:slug>', views.serie, name='serie'),
    path('kaydet_serie/<int:serie_id>/', views.kaydet_serie, name='kaydet_serie'),
    path('kayitlar_serie', views.kayitlar_serie, name='kayitlar_serie'),
    
    
    # Authentication
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('profil',views.profile, name='profil'),
    path('change_password/', change_password, name='change_password'),
    path('reset_saves/<int:user_id>/', reset_user_saves, name='reset_saves'),
    
    
    # Recommendation
    path('reco', views.reco, name='reco'),
    
    
    # Count
    ]


