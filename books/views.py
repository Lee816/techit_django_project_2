from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render ,get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import redis
from django.conf import settings

from .models import Book, Books_rental, Category, Review
from .forms import ReviewForm
from .tasks import return_email

# Create your views here.

redi = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
# 추천 시스템 ( 사용자가 자주 대여하는 카테고리 내의 평점이 높은 책)
def recommendbook(user):
    # 카테고리 별 대여 횟수
    categories = {category.name : 0 for category in list(Category.objects.all())}
    
    for rental in list(Books_rental.objects.filter(user=user)):
        categories[rental.book.category.name] += 1
    
    # 카테고리 별 대여 횟수 redis 등록
    redi.zadd(name='category_rank', mapping=categories)
    
    # 대여 횟수가 제일 많은 카테고리 반환
    recommend_category = redi.zrevrange(name='category_rank',start=0,end=-1,withscores=True)[0][0].decode('utf-8')

    # 추천 카테고리 책 별 평점
    books = Book.objects.filter(category__name=recommend_category)
    recommend_books = {book.title : 0 for book in books}

    for book in books:
        reviews = Review.objects.filter(book=book)
        if reviews:
            recommend_books[book.title] = sum([review.grade for review in reviews])/len(reviews)

    # 추천 카테고리 책 평점 redis 등록
    redi.zadd(name='book_rank', mapping=recommend_books)
    
    # 평점이 높은 책 5권 반환
    rank_books = {}
    for item in redi.zrevrange(name='book_rank',start=0,end=5, withscores=True):
        rank_books[item[0].decode('utf-8')] = item[1]
    
    return recommend_category, rank_books

def HomePage(request):
    latest_books = Book.objects.all().order_by('-created')[:5]
    like_books = Book.objects.all().order_by('-like')[:5]
    
    if not request.user.is_anonymous :
        recommend_category,rank_books = recommendbook(request.user)
    else:
        recommend_category = None
        rank_books = None
    
    return render(request, 'home.html',{'latest_books':latest_books,'like_books':like_books, 'recommend_category':recommend_category, 'rank_books':rank_books})

class BooksList(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/books_list.html'
    
    paginate_by = 4
    
def CategoryBooksList(request, category_id):
    books = Book.objects.filter(category=category_id)
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'books/books_list.html', {'books':books, 'category':category})
    
class BookDetail(generic.DetailView):
    model = Book
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewform'] = ReviewForm()
        reviews = Review.objects.filter(book=kwargs['object'])
        if reviews:
            context["reviews"] = reviews
            context['review_aver'] = sum([review.grade for review in reviews])/len(reviews)
        if self.request.user.is_authenticated:
            context['can_review'] = Books_rental.objects.filter(book=kwargs['object'],user=self.request.user)
        return context

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Book
    fields = ['category','title','author','publisher','stock','summary']
    context_object_name = 'form'
    redirect_field_name = 'accounts:login'
    template_name = 'books/book_create.html'
    permission_required = 'books.add_book'
    success_url = reverse_lazy('books:books_list')
    
class RentalBooksList(LoginRequiredMixin, generic.ListView):
    model = Books_rental
    context_object_name = 'rental_books'
    template_name = 'books/rental_list.html'
    redirect_field_name = 'accounts/login'
    
    def get_queryset(self):
        return Books_rental.objects.filter(user=self.request.user, book_return=False)

@login_required
def BookRent(request, book_id):
    if request.user.is_anonymous :
        return redirect('accounts:login')
    else:
        book = get_object_or_404(Book, id=book_id)
        if book.stock > 0 :
            Books_rental.objects.create(user=request.user,book=book,rental_date=timezone.localdate(),return_date=timezone.localdate()+timezone.timedelta(weeks=1))
            book.stock -= 1
            book.like += 1
            book.save()
            return redirect('books:my_rentals')
        else:
            return redirect('books:books_list')

@login_required
def BookReturn(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        rental_book = Books_rental.objects.filter(book=book, user=request.user, book_return=False).first()
        book.stock += 1
        rental_book.book_return = True
        book.save()
        rental_book.save()
        
        # 비동기 반납 메일 보내기
        return_email.delay(book_id)
        
    return redirect('books:my_rentals')

@login_required
def BookReturnList(request):
    if request.user.is_superuser:
        not_rental_books = Books_rental.objects.filter(book_return=False, return_date__lt=timezone.localdate())
        return render(request, 'books/not_return_list.html', {'not_rental_books':not_rental_books})
    else:
        return redirect('books:books_list')

def BookSearch(request):
    word = request.GET.get('word')
    books = Book.objects.filter(Q(title__icontains=word)|Q(author__icontains=word))
    
    paginator = Paginator(books, 4)
    
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'books/books_list.html', {
        'word': word,
        'books': page.object_list,
        'page_obj': page,
        'paginator': paginator,
    })
    
@login_required
@require_POST
def ReviewAdd(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    rental_book = Books_rental.objects.filter(user=request.user, book=book)
    form = ReviewForm(data=request.POST)
    
    # 대여기록이 있으면 리뷰 작성 가능
    if rental_book:
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
        
    return redirect('books:book_detail', book_id)