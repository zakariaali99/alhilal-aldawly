from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardIndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Livestock
    path('livestock/', views.LivestockListView.as_view(), name='livestock_list'),
    path('livestock/add/', views.LivestockCreateView.as_view(), name='livestock_create'),
    path('livestock/<int:pk>/edit/', views.LivestockUpdateView.as_view(), name='livestock_edit'),
    path('livestock/<int:pk>/delete/', views.LivestockDeleteView.as_view(), name='livestock_delete'),
    path('livestock/<int:pk>/gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    path('livestock/<int:pk>/gallery/add/', views.GalleryCreateView.as_view(), name='gallery_create'),
    path('gallery/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # News
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/comments/', views.NewsCommentsView.as_view(), name='news_comments'),
    path('news/comment/<int:pk>/approve/', views.ApproveCommentView.as_view(), name='comment_approve'),
    path('news/comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='comment_delete'),
    
    # Messages
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    
    # Hero Sections
    path('heroes/', views.HeroListView.as_view(), name='hero_list'),
    path('heroes/add/', views.HeroCreateView.as_view(), name='hero_create'),
    path('heroes/<int:pk>/edit/', views.HeroUpdateView.as_view(), name='hero_edit'),
    path('heroes/<int:pk>/delete/', views.HeroDeleteView.as_view(), name='hero_delete'),
    
    # Settings
    path('settings/', views.SettingsUpdateView.as_view(), name='settings'),
    
    # Backup
    path('backup/', views.BackupView.as_view(), name='backup'),
]
