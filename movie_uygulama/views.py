from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Actors , Director, Category, Save , Books, Writers, Series, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count 
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .forms import ProfileForm
from .rv import recommend_RV


#Movies
def films(request):
    filmler = Movie.objects.all()
    saved_movie_ids = []
    if request.user.is_authenticated:
        saved_movie_ids = Save.objects.filter(user=request.user).values_list('movie_id', flat=True)

    context = {
        "filmler": filmler,
        "saved_movie_ids": saved_movie_ids
    }
    return render(request, 'films.html', context)
@login_required(login_url='login')
def kaydet(request, movie_id):
    
    movie = get_object_or_404(Movie, id=movie_id)
    kayit, created = Save.objects.get_or_create(user=request.user, movie=movie)
    referer = request.META.get('HTTP_REFERER', '')
    if not created:
        kayit.delete()
        if 'film' in referer:
            return redirect('film', slug=movie.slug)
        elif 'kayitlar' in referer:
            return redirect('kayitlar')
        else:
            return redirect('films')
    if 'film' in referer:
        return redirect('film', slug=movie.slug)
    elif 'kayitlar' in referer:
        return redirect('kayitlar')
    else:
        return redirect('films')
@login_required(login_url='login')
def kayitlar(request):
    filmler = Movie.objects.all()
    if request.user.is_authenticated:
        saved_movie_ids = Save.objects.filter(user=request.user).values_list('movie_id', flat=True)
    context = {
        "filmler": filmler,
        "saved_movie_ids": saved_movie_ids
    }
    return render(request, 'kayıtlı_filmler.html',context)
@login_required(login_url='login')
def film(request,slug):
    filmler = get_object_or_404(Movie,slug=slug)
    if request.user.is_authenticated:
        saved_movie_ids = Save.objects.filter(user=request.user).values_list('movie_id', flat=True)
    context = {
        "filmler": filmler,
        "saved_movie_ids": saved_movie_ids
    }
    return render(request, 'film.html', context)
#Books
def books(request):
    kitaplar = Books.objects.all()
    saved_book_ids = []
    if request.user.is_authenticated:
        saved_book_ids = Save.objects.filter(user=request.user).values_list('book_id', flat=True)
        
    context = {
        "kitaplar": kitaplar,
        "saved_book_ids": saved_book_ids
    }
    return render(request, 'books.html',context)
@login_required(login_url='login')
def kaydet_kitap(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    kayit2, created2 = Save.objects.get_or_create(user=request.user, book=book)
    referer = request.META.get('HTTP_REFERER', '')
    if not created2:
        kayit2.delete()
        if 'books' in referer:
            return redirect('books')
        elif 'kayitlar_kitap' in referer:
            return redirect('kayitlar_kitap')
        else:
            return redirect('kitap', slug=book.slug)
    if 'books' in referer:
        return redirect('books')
    elif 'kayitlar_kitap' in referer:
        return redirect('kayitlar_kitap')
    else:
        return redirect('kitap', slug=book.slug)
@login_required(login_url='login')
def kayitlar_kitap(request):
    kitaplar = Books.objects.all()
    if request.user.is_authenticated:
        saved_book_ids = Save.objects.filter(user=request.user).values_list('book_id', flat=True)
    context = {
        "kitaplar": kitaplar,
        "saved_book_ids": saved_book_ids
    }
    return render(request, 'kayıtlı_kitaplar.html',context)
@login_required(login_url='login')
def kitap(request,slug):
    kitaplar = get_object_or_404(Books,slug=slug)
    if request.user.is_authenticated:
        saved_book_ids = Save.objects.filter(user=request.user).values_list('book_id', flat=True)
    context = {
        "kitaplar": kitaplar,
        "saved_book_ids": saved_book_ids
    }
    return render(request, 'kitap.html', context)
#Series
def series(request):
    diziler = Series.objects.all()
    saved_serie_ids = []
    if request.user.is_authenticated:
        saved_serie_ids = Save.objects.filter(user=request.user).values_list('serie_id', flat=True)

    context = {
        "diziler": diziler,
        "saved_serie_ids": saved_serie_ids
    }
    return render(request, 'series.html', context)
@login_required(login_url='login')
def kaydet_serie(request, serie_id):
    
    serie = get_object_or_404(Series, id=serie_id)
    kayit3, created3 = Save.objects.get_or_create(user=request.user, serie=serie)
    referer = request.META.get('HTTP_REFERER', '')
    if not created3:
        kayit3.delete()
        if 'series' in referer:
            return redirect('series')
        elif 'kayitlar_serie' in referer:
            return redirect('kayitlar_serie')
        else:
            return redirect('serie', slug=serie.slug)
    if 'series' in referer:
        return redirect('series')
    elif 'kayitlar_serie' in referer:
        return redirect('kayitlar_serie')
    else:
        return redirect('serie', slug=serie.slug)
@login_required(login_url='login')
def kayitlar_serie(request):
    diziler = Series.objects.all()
    if request.user.is_authenticated:
        saved_serie_ids = Save.objects.filter(user=request.user).values_list('serie_id', flat=True)
    context = {
        "diziler": diziler,
        "saved_serie_ids": saved_serie_ids
    }
    return render(request, 'kayıtlı_diziler.html',context)
@login_required(login_url='login')
def serie(request,slug):
    diziler = get_object_or_404(Series,slug=slug)
    if request.user.is_authenticated:
        saved_serie_ids = Save.objects.filter(user=request.user).values_list('serie_id', flat=True)
    context = {
        "diziler": diziler,
        "saved_serie_ids": saved_serie_ids
    }
    return render(request, 'serie.html',context)






#Home
def index(request):
    return render(request, 'index.html')



def actor(request,slug):
    actors = get_object_or_404(Actors,slug=slug)
    movie = Movie.objects.filter(actors=actors)
    series = Series.objects.filter(actors=actors)
    context = {
        "actors": actors,
        "movie": movie,
        "series": series
    }
    return render(request, 'actor.html', context)

def director(request,slug):
    directors = get_object_or_404(Director,slug=slug)
    movie = Movie.objects.filter(director=directors)
    series = Series.objects.filter(director=directors)
    context = {
        "dir": directors,
        "movie": movie,
        "series": series
    }
    return render(request, 'director.html', context)

def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {"categories": categories})

def yazar(request,slug):
    yazarlar = get_object_or_404(Writers,slug=slug)
    kitaplar = Books.objects.filter(yazar=yazarlar)
    context = {
        "yazar": yazarlar,
        "kitaplar": kitaplar
    }
    return render(request, 'yazar.html', context)
#Serie









#User 

def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login (request, user)
            return redirect('index')
        else:
            return render(request, 'login_page.html', {"error": "Kullanıcı adı veya şifre hatalı"})
    else:
        return render(request, 'login_page.html')

def register_request(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        email = request.POST.get('email', '')
        
        if password != repassword:
            return render(request, 'register_page.html', {"error": "Şifreler uyuşmuyor"})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register_page.html', {"error": "Kullanıcı adı zaten var"})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register_page.html', {"error": "Email zaten var"})
        
        user = User.objects.create_user(username, email, password)
        user.save()
        return render(request, 'login_page.html')
                
    return render(request, 'register_page.html')
    
    
    
@login_required(login_url='login')
def reset_user_saves(request, user_id):
    if request.method == 'POST' and request.user.id == user_id:
        Save.objects.filter(user_id=user_id).delete()
        return redirect('profil')


def logout_request(request):
	logout(request)
	return redirect('index')








@csrf_exempt
@login_required(login_url='login')
def reco(request):
    if request.method == 'GET':
        request.session['reco_state'] = {"step": 0, "selection": None}
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_message = body.get('message', '').strip()

            if not user_message:
                return JsonResponse({'result': "I didn't catch that."})
            session_data = request.session.get('reco_state', {"step": 0, "selection": None})
            bot_reply = recommend_RV(user_message)  
            request.session['reco_state'] = session_data

            return JsonResponse({'result': bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        

    return render(request, 'reco.html')


    
    
    
    
    
    
    


@login_required(login_url='login')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'update_image' in request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = ProfileForm(instance=profile)

    if request.method == 'POST' and 'delete_account' in request.POST:
        user = request.user
        user.delete()
        return redirect('login')

    saved_movie_ids = Save.objects.filter(user=request.user, movie__isnull=False).values_list('movie_id', flat=True)
    category_counts = (
        Movie.objects.filter(id__in=saved_movie_ids)
        .values('category__name')
        .annotate(count=Count('category'))
        .order_by('-count')[:3]
    )

    saved_serie_ids = Save.objects.filter(user=request.user, serie__isnull=False).values_list('serie_id', flat=True)
    category_counts2 = (
        Series.objects.filter(id__in=saved_serie_ids)
        .values('category__name')
        .annotate(count=Count('category'))
        .order_by('-count')[:3]
    )

    saved_book_ids = Save.objects.filter(user=request.user, book__isnull=False).values_list('book_id', flat=True)
    category_counts3 = (
        Books.objects.filter(id__in=saved_book_ids)
        .values('bookCategories__name')  
        .annotate(count=Count('bookCategories'))
        .order_by('-count')[:3]
    )

    
    category_counts_list = list(category_counts)
    category_counts_json = json.dumps(category_counts_list)

    category_counts2_list = list(category_counts2)
    category_counts2_json = json.dumps(category_counts2_list)
    
    category_counts3_list = list(category_counts3)
    category_counts3_json = json.dumps(category_counts3_list)
    
    

    context = {
        "profile": profile,
        "form": form,  
        "category_counts_json": category_counts_json,
        "category_counts2_json": category_counts2_json,
        "category_counts3_json": category_counts3_json
    }

    return render(request, "profile.html", context)





@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Oturumun açık kalmasını sağlar
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect('login')  # Başarıyla değiştikten sonra yönlendirme
        else:
            messages.error(request, 'Lütfen formdaki hataları düzeltin.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})






