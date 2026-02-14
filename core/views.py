from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import HeroSection, SiteSettings, ContactMessage
from livestock.models import LivestockItem
from news.models import Article

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heroes'] = HeroSection.objects.filter(is_active=True)
        context['featured_livestock'] = LivestockItem.objects.all()[:4]
        context['recent_articles'] = Article.objects.filter(is_published=True)[:3]
        return context

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
        return redirect('core:contact')
