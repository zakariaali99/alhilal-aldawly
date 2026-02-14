from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Article, Commenter, Comment

class NewsListView(ListView):
    model = Article
    template_name = "news/list.html"
    context_object_name = "articles"
    queryset = Article.objects.filter(is_published=True)

class NewsDetailView(DetailView):
    model = Article
    template_name = "news/detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['approved_comments'] = article.comments.filter(is_approved=True)
        context['approved_comments_count'] = context['approved_comments'].count()
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        if name and email and content:
            commenter, created = Commenter.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
            Comment.objects.create(
                article=article,
                commenter=commenter,
                content=content
            )
        return redirect('news:detail', slug=article.slug)
