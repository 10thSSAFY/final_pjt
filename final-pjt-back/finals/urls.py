from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list),  # GET: 조회, POST: 생성 (관리자만 가능해야 함)
    path('posts/', views.post_list),  # GET, POST
    path('posts/<int:post_pk>/', views.post_detail),  # GET, PUT, DELETE
    path('posts/<int:post_pk>/comments/', views.comment_create),  # POST
    path('comments/<int:comment_pk>/', views.comment_delete),  # DELETE
    path('save-deposit-products/', views.save_deposit_products),  # GET
    path('deposits/', views.deposit_list), # GET
    path('deposits/<int:deposit_pk>/', views.deposit_detail), # GET
    path('deposits/<int:deposit_pk>/join/', views.deposit_join),  # GET
    path('deposits/recommend/', views.deposit_recomend), # GET
    path('saves/', views.save_list), # GET
    path('saves/<int:save_pk>/', views.save_detail), # GET
    path('saves/recommend/', views.save_recomend), # GET
    path('exchanges/', views.exchanges),  # GET
    path('saves/<int:save_pk>/join/', views.save_join),  # GET
    path('join_info/', views.get_user_products)  # GET
]
