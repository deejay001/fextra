from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('vendors/', views.vendors, name='vend'),
    path('contact/', views.contact, name='contact'),
    path('how-it-works/', views.how, name='how'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('log_in/', views.log_in, name='log_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
]

urlpatterns += [
    path('home', views.home_page, name='home'),
    path('invest', views.invest, name='invest'),
    path('withdraw/<w_name>', views.withdraw, name='w_draw'),
    path('log_out/', views.log_out, name='log_out'),
]

urlpatterns += [
    path('admin_login', views.admine_login, name='a_login'),
    path('admin_dashboard', views.admine_page, name='admine'),
    path('withdrawals/<w_name>', views.check_with, name='c_with'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
