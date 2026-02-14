from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from core.models import ContactMessage, HeroSection, SiteSettings
from livestock.models import LivestockItem, Category, MediaGalleryItem
from news.models import Article, Comment

class DashboardMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_messages_count'] = ContactMessage.objects.filter(is_read=False).count()
        return context

class DashboardIndexView(DashboardMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'messages': ContactMessage.objects.count(),
            'unread_messages': context['unread_messages_count'],
            'livestock': LivestockItem.objects.count(),
            'articles': Article.objects.count(),
        }
        context['recent_messages'] = ContactMessage.objects.all()[:5]
        context['recent_articles'] = Article.objects.all()[:5]
        return context

class SearchView(DashboardMixin, TemplateView):
    template_name = 'dashboard/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        
        if query:
            context['livestock_results'] = LivestockItem.objects.filter(
                Q(title_ar__icontains=query) | 
                Q(title_en__icontains=query) |
                Q(description_ar__icontains=query)
            )
            context['news_results'] = Article.objects.filter(
                Q(title_ar__icontains=query) | 
                Q(title_en__icontains=query) |
                Q(content_ar__icontains=query)
            )
        else:
            context['livestock_results'] = []
            context['news_results'] = []
            
        return context

# Livestock Views
class LivestockListView(DashboardMixin, ListView):
    model = LivestockItem
    template_name = 'dashboard/livestock_list.html'
    context_object_name = 'items'
    paginate_by = 10

class LivestockCreateView(DashboardMixin, CreateView):
    model = LivestockItem
    template_name = 'dashboard/livestock_form.html'
    fields = ['category', 'title_ar', 'title_en', 'slug', 'description_ar', 'description_en', 'featured_image', 'is_featured']
    success_url = reverse_lazy('dashboard:livestock_list')

class LivestockUpdateView(DashboardMixin, UpdateView):
    model = LivestockItem
    template_name = 'dashboard/livestock_form.html'
    fields = ['category', 'title_ar', 'title_en', 'slug', 'description_ar', 'description_en', 'featured_image', 'is_featured']
    success_url = reverse_lazy('dashboard:livestock_list')

class LivestockDeleteView(DashboardMixin, DeleteView):
    model = LivestockItem
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:livestock_list')

# Category Views
class CategoryListView(DashboardMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'

from .forms import CategoryForm

class CategoryCreateView(DashboardMixin, CreateView):
    model = Category
    template_name = 'dashboard/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category_list')

class CategoryUpdateView(DashboardMixin, UpdateView):
    model = Category
    template_name = 'dashboard/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category_list')

class CategoryDeleteView(DashboardMixin, DeleteView):
    model = Category
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:category_list')

# News Views
class NewsListView(DashboardMixin, ListView):
    model = Article
    template_name = 'dashboard/news_list.html'
    context_object_name = 'articles'
    paginate_by = 10

class NewsCreateView(DashboardMixin, CreateView):
    model = Article
    template_name = 'dashboard/news_form.html'
    fields = ['title_ar', 'title_en', 'slug', 'content_ar', 'content_en', 'featured_image', 'is_published']
    success_url = reverse_lazy('dashboard:news_list')

class NewsUpdateView(DashboardMixin, UpdateView):
    model = Article
    template_name = 'dashboard/news_form.html'
    fields = ['title_ar', 'title_en', 'slug', 'content_ar', 'content_en', 'featured_image', 'is_published']
    success_url = reverse_lazy('dashboard:news_list')

class NewsDeleteView(DashboardMixin, DeleteView):
    model = Article
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:news_list')

class NewsCommentsView(DashboardMixin, DetailView):
    model = Article
    template_name = 'dashboard/news_comments.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().select_related('commenter')
        return context

class ApproveCommentView(DashboardMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = True
        comment.save()
        return HttpResponseRedirect(reverse('dashboard:news_comments', args=[comment.article.pk]))

class DeleteCommentView(DashboardMixin, DeleteView):
    model = Comment
    template_name = 'dashboard/confirm_delete.html'

    def get_success_url(self):
        return reverse('dashboard:news_comments', args=[self.object.article.pk])

# Message Views
class MessageListView(DashboardMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/messages.html'
    context_object_name = 'messages'
    paginate_by = 15

class MessageDetailView(DashboardMixin, DetailView):
    model = ContactMessage
    template_name = 'dashboard/message_detail.html'
    context_object_name = 'message'

    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

class MessageDeleteView(DashboardMixin, DeleteView):
    model = ContactMessage
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:message_list')

# Hero Section Views
class HeroListView(DashboardMixin, ListView):
    model = HeroSection
    template_name = 'dashboard/hero_list.html'
    context_object_name = 'heroes'

class HeroCreateView(DashboardMixin, CreateView):
    model = HeroSection
    template_name = 'dashboard/hero_form.html'
    fields = ['title_ar', 'title_en', 'subtitle_ar', 'subtitle_en', 'image', 'cta_text_ar', 'cta_text_en', 'cta_link', 'is_active', 'order']
    success_url = reverse_lazy('dashboard:hero_list')

class HeroUpdateView(DashboardMixin, UpdateView):
    model = HeroSection
    template_name = 'dashboard/hero_form.html'
    fields = ['title_ar', 'title_en', 'subtitle_ar', 'subtitle_en', 'image', 'cta_text_ar', 'cta_text_en', 'cta_link', 'is_active', 'order']
    success_url = reverse_lazy('dashboard:hero_list')

class HeroDeleteView(DashboardMixin, DeleteView):
    model = HeroSection
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:hero_list')

# Settings View
class SettingsUpdateView(DashboardMixin, UpdateView):
    model = SiteSettings
    template_name = 'dashboard/settings_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard:index')

    def get_object(self):
        return SiteSettings.objects.first() or SiteSettings.objects.create(email='info@alhilal.ly')

# Gallery Views
class GalleryListView(DashboardMixin, ListView):
    model = MediaGalleryItem
    template_name = 'dashboard/gallery_list.html'
    context_object_name = 'gallery_items'

    def get_queryset(self):
        self.livestock_item = get_object_or_404(LivestockItem, pk=self.kwargs['pk'])
        return MediaGalleryItem.objects.filter(livestock_item=self.livestock_item).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livestock_item'] = self.livestock_item
        return context

class GalleryCreateView(DashboardMixin, CreateView):
    model = MediaGalleryItem
    template_name = 'dashboard/gallery_form.html'
    fields = ['media_type', 'file', 'caption_ar', 'caption_en', 'order']

    def form_valid(self, form):
        form.instance.livestock_item = get_object_or_404(LivestockItem, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:gallery_list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livestock_item'] = get_object_or_404(LivestockItem, pk=self.kwargs['pk'])
        return context

class GalleryDeleteView(DashboardMixin, DeleteView):
    model = MediaGalleryItem
    template_name = 'dashboard/confirm_delete.html'

    def get_success_url(self):
        return reverse('dashboard:gallery_list', kwargs={'pk': self.object.livestock_item.pk})

class BackupView(DashboardMixin, View):
    """Create and download a complete backup of the system"""
    
    def get(self, request):
        import os
        import shutil
        from django.http import HttpResponse, FileResponse
        from django.conf import settings
        from datetime import datetime
        import zipfile
        from pathlib import Path
        
        # Create backup directory
        backup_dir = Path(settings.BASE_DIR) / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for backup name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'alhilal_backup_{timestamp}'
        backup_path = backup_dir / f'{backup_name}.zip'
        
        # Create ZIP file
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Backup database
            db_path = Path(settings.BASE_DIR) / 'db.sqlite3'
            if db_path.exists():
                zipf.write(db_path, 'db.sqlite3')
            
            # Backup media files
            media_root = Path(settings.MEDIA_ROOT)
            if media_root.exists():
                for file_path in media_root.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(settings.BASE_DIR)
                        zipf.write(file_path, arcname)
        
        # Serve the file for download
        response = FileResponse(open(backup_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{backup_name}.zip"'
        
        return response
