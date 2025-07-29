from django.contrib import admin
from django.urls import path, include
from Bookshelf import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),  # přidat tento řádek
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
