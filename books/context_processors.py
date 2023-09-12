from .models import Category

def get_categories(self):
    categories = Category.objects.all()
    return {'categories':categories}