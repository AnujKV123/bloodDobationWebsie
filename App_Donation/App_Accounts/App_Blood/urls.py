from django.urls import path
from App_Blood import views
app_name='App_Blood'
urlpatterns = [
    path('',views.index,name='index'),
    path('about-us', views.About, name='about'),
    path('blog', views.Blog, name='blog'),
    path('blog/details/<int:id>',views.Blogdetails,name='blog_details'),
    path('contact-us', views.Contact, name='contact'),
    path('doner', views.Doner, name='doner'),
    path('gallery',views.Gallery,name='gallery'),
    path('privacy',views.Privacy,name='privacy'),
    path('blog-like',views.blog_like,name='bloglike'),
    path('branches',views.Brancheview,name='branches'),
    path('single-path/<int:id>',views.SingleBranch,name='single_branch'),
    path('doner-details/<int:id>',views.Donardetails,name='doner_details'),

]
