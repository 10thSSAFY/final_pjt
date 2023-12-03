from rest_framework import serializers
from .models import  Category, Post, Comment, DepositBaseList, DepositOptionList, SaveBaseList, SaveOptionList, ExchangeList
from django.contrib.auth import get_user_model 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class UserNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)
    user = UserNameSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user',)


class PostListSerializer(serializers.ModelSerializer):
    class UsernameSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)
    user = UsernameSerializer(read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class DepositOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptionList
        fields = '__all__'
        read_only_fields = ('baselist',)

        
class DepositBaseListSerializer(serializers.ModelSerializer):
    depositoptionlist_set = DepositOptionListSerializer(many=True, read_only=True)
    class Meta:
        model = DepositBaseList
        fields = '__all__'


class DepositBaseListDetailSerializer(serializers.ModelSerializer):
    depositoptionlist_set = DepositOptionListSerializer(many=True, read_only=True)
    class Meta:
        model = DepositBaseList
        fields = '__all__'


class SaveOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveOptionList
        fields = '__all__'
        read_only_fields = ('baselist',)


class SaveBaseListSerializer(serializers.ModelSerializer):
    saveoptionlist_set = SaveOptionListSerializer(many=True, read_only=True)
    class Meta:
        model = SaveBaseList
        fields = '__all__'


class SaveBaseListDetailSerializer(serializers.ModelSerializer):
    saveoptionlist_set = SaveOptionListSerializer(many=True, read_only=True)
    class Meta:
        model = SaveBaseList
        fields = '__all__'


class ExchangeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeList
        fields = '__all__'