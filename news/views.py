from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import News, Category
from .forms import NewsForm


class HomeNews(ListView):
    model = News                                   # Cвязь с моделькой News
    template_name = 'news/home_news_list.html'     # django по умолчанию ищет list_viev.html, а мы переопределили
    context_object_name = 'news'                   # переопределяем object_list
    # extra_context = {'title': 'Это я так захотел'} # название на вкладке
    def get_context_data(self, *, object_list=None, **kwargs):  # Это то что и extra_context, название на вкладке
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)

class GetNewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):  # Это то что и extra_context, название на вкладке
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.filter(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)





# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect('/')
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})