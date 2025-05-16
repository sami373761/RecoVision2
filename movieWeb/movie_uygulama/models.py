from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images",default='profile_images/default.jpg')
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Movie(models.Model):
    category = models.ManyToManyField('Category', blank=True) 
    director = models.ForeignKey('Director', on_delete=models.CASCADE ,null=True,blank=True)
    actors = models.ManyToManyField('Actors',  blank=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    year = models.IntegerField()
    imdb_rating = models.FloatField()
    image = models.ImageField(upload_to='movie_images')
    slug = models.SlugField(unique=True, null = True, blank = True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Movies"
        

class Director(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='director_images')
    slug = models.SlugField(unique=True, null = True, blank = True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Directors"
        
class Actors(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='actor_images')
    slug = models.SlugField(unique=True, null = True, blank = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Actors"
        verbose_name = "Actor"
        

class Category(models.Model):
    keyword = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
    
    

    
    
class Save(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey('Books', on_delete=models.CASCADE, null=True, blank=True)
    serie = models.ForeignKey('Series', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_movie'),
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book'),
            models.UniqueConstraint(fields=['user', 'serie'], name='unique_user_serie'),
        ]

    def __str__(self):
        return f"{self.user} saved {self.movie or self.book or self.serie}"

    
    
    
class Books(models.Model):
    bookCategories = models.ManyToManyField('BookCategory',  blank=True)
    title = models.CharField(max_length=100)
    yazar = models.ForeignKey('Writers', on_delete=models.CASCADE ,null=True,blank=True)
    description = models.TextField()
    year = models.IntegerField()
    image = models.ImageField(upload_to='book_images')
    slug = models.SlugField(unique=True, null = True, blank = True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Books"
        

class Writers(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='writer_images')
    slug = models.SlugField(unique=True, null = True, blank = True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Writers"
        
class BookCategory(models.Model):
    keyword = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_category_images', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Book Categories"
        verbose_name = "Book Category"
        
class Series(models.Model):
    category = models.ManyToManyField('Category', blank=True)    
    actors = models.ManyToManyField('Actors',  blank=True)
    description = models.TextField()
    year = models.IntegerField()
    imdb_rating = models.FloatField()
    image = models.ImageField(upload_to='series_images')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank = True)
    director = models.ForeignKey('Director', on_delete=models.CASCADE ,null=True,blank=True)
    director_cast = models.ManyToManyField('Director', blank=True, related_name='director_cast')
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Series"
        

