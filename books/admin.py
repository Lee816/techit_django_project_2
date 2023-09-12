from django.contrib import admin

from .models import Book, Books_rental, Category

# Register your models here.

admin.site.register(Category)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','category','author','stock','created']
    list_filter = ['author']
    search_fields = ['title','author']

@admin.register(Books_rental)
class BooksRentalAdmin(admin.ModelAdmin):
    list_display = ['user','book','rental_date','return_date']
    list_filter = ['user','book','rental_date','return_date']
    search_fields = ['user','book']