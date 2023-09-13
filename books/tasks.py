from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Books_rental

@shared_task
def return_email(book_id):
    # 객체 찾기
    rental_book = Books_rental.objects.get(book__id=book_id)
    
    # 메일 보내기
    subject = f'Book Title : [{rental_book.book.title}]'
    message = f'Dear {rental_book.user.username},\n\n The book has been returned successfully on {timezone.localdate()}.'
    mail_sent = send_mail(subject,message,'Track@Library.com',[rental_book.user.email])

    return mail_sent