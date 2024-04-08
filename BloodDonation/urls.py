from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from ckeditor_uploader.views import upload
from ckeditor_uploader import views
from django.views.decorators.cache import never_cache
from django.views.static import serve

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.site.site_header = 'BloodLab Admin'
admin.site.site_title = 'Welcome to BloodLab'
urlpatterns = [
    path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path>', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('',include('App_Blood.urls')),
    path('accounts/',include('App_Accounts.urls')),
    path('ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()