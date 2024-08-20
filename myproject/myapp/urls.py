from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('referrals/', views.referral_list, name='referral_list'),
    path('referred_by/', views.referred_by, name='referred_by'),
    # path('logout/', views.user_logout, name='logout'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('decorative_profile/', views.decorative_profile, name='decorative_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/apply/', views.apply_for_product, name='apply_for_product'),
    path('product/new/', views.create_product, name='create_product'),

    path('post_list/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),  
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/new/', views.create_post, name='create_post'),

    path('withdraw/', views.withdraw_points, name='withdraw_points'),
    path('ledger/', views.ledger, name='ledger'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('toggle-permission/<int:user_id>/<str:permission>/', views.toggle_permission, name='toggle_permission'),
    path('process-withdrawal/<int:withdrawal_id>/', views.process_withdrawal, name='process_withdrawal'),
]