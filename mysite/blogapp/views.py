from django.views.generic import ListView

from .models import Article


class ArticlesListView(ListView):
    queryset = Article.objects.defer("content").select_related("author", 'category', 'tag').all()
    context_object_name = 'articles'

    class Meta:
        ordering = ['name']
