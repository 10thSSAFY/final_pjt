from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.conf import settings
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Post, Comment, DepositBaseList, DepositOptionList, ExchangeList, SaveBaseList, SaveOptionList
from accounts.models import User
from .serializers import CategorySerializer, PostSerializer, PostListSerializer, CommentSerializer, ExchangeListSerializer
from .serializers import DepositBaseListSerializer, DepositOptionListSerializer, DepositBaseListDetailSerializer
from .serializers import SaveBaseListSerializer, SaveOptionListSerializer, SaveBaseListDetailSerializer
import requests

# Create your views here.
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = get_list_or_404(Post)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({"message": "인증 자격 증명이 제공되지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PostListSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if post.user.pk != request.user.pk:
            return Response({"message": "권한 자격 증명이 제공되지 않았습니다."}, status=status.HTTP_403_UNAUTHORIZED)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if post.user.pk != request.user.pk:
            return Response({"message": "권한 자격 증명이 제공되지 않았습니다."}, status=status.HTTP_403_UNAUTHORIZED)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user.pk != request.user.pk:
            return Response({"message": "권한 자격 증명이 제공되지 않았습니다."}, status=status.HTTP_403_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.PRODUCT_API_KEY
    deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    save_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    deposit_res = requests.get(deposit_url).json()
    save_res = requests.get(save_url).json()

    for deposit_data in deposit_res.get('result').get('baseList'):
        if DepositBaseList.objects.filter(fin_prdt_cd = deposit_data.get('fin_prdt_cd')).exists():
            continue
        serializer = DepositBaseListSerializer(data = deposit_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    for save_data in save_res.get('result').get('baseList'):
        if SaveBaseList.objects.filter(fin_prdt_cd = save_data.get('fin_prdt_cd')).exists():
            continue
        serializer = SaveBaseListSerializer(data = save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    for li in deposit_res.get("result").get("optionList"):
        save_optionlist = {
            'intr_rate_type': li.get('intr_rate_type'),
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'save_trm': li.get('save_trm'),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
        }
        serializer = DepositOptionListSerializer(data = save_optionlist)
        product = DepositBaseList.objects.get(fin_prdt_cd = li.get('fin_prdt_cd'))

        if not DepositOptionList.objects.filter(
            baselist = product.id,
            intr_rate_type = save_optionlist['intr_rate_type'],
            intr_rate_type_nm = save_optionlist['intr_rate_type_nm'],
            save_trm = save_optionlist['save_trm'],   
            intr_rate = save_optionlist['intr_rate'],
            intr_rate2 = save_optionlist['intr_rate2']
            ).exists():
            if serializer.is_valid(raise_exception=True):
                serializer.save(baselist=product)

    for li in save_res.get("result").get("optionList"):

        save_optionlist = {
            'intr_rate_type': li.get('intr_rate_type'),
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'rsrv_type': li.get('rsrv_type'),
            'rsrv_type_nm': li.get('rsrv_type_nm'),
            'save_trm': li.get('save_trm'),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
        }
        serializer = SaveOptionListSerializer(data = save_optionlist)
        product = SaveBaseList.objects.get(fin_prdt_cd = li.get('fin_prdt_cd'))

        if not SaveOptionList.objects.filter(
            baselist = product.id,
            intr_rate_type = save_optionlist['intr_rate_type'],
            intr_rate_type_nm = save_optionlist['intr_rate_type_nm'],
            rsrv_type = save_optionlist['rsrv_type'],
            rsrv_type_nm = save_optionlist['rsrv_type_nm'],
            save_trm = save_optionlist['save_trm'],   
            intr_rate = save_optionlist['intr_rate'],
            intr_rate2 = save_optionlist['intr_rate2']
            ).exists():
            if serializer.is_valid(raise_exception=True):
                serializer.save(baselist=product)

    return Response({'message': 'okay'})


@api_view(['GET'])
def deposit_list(request):
    if request.method == 'GET':
        products = get_list_or_404(DepositBaseList)
        serializer = DepositBaseListSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def deposit_detail(request, deposit_pk):    
    products = get_object_or_404(DepositBaseList, pk=deposit_pk)
    print(deposit_pk)
    if request.method == 'GET':
        print(1)
        serializer = DepositBaseListDetailSerializer(products)
        return Response(serializer.data)
    

@api_view(['GET'])
def save_list(request):
    if request.method == 'GET':
        products = get_list_or_404(SaveBaseList)
        serializer = SaveBaseListSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def save_detail(request, save_pk):
    products = get_object_or_404(SaveBaseList, pk=save_pk)
    if request.method == 'GET':
        serializer = SaveBaseListDetailSerializer(products)
        return Response(serializer.data)


@api_view(['GET'])
def exchanges(request):
    api_key = settings.EXCHANGE_API_KEY
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate=20180102&data=AP01'
    res = requests.get(url).json()
    valid_res = []
    for exchange_data in res:
        if ExchangeList.objects.filter(cur_unit = exchange_data.get('cur_unit')).exists():
            valid_res.append(exchange_data)  # 이미 존재하는 데이터는 valid_res 리스트에 추가합니다.
            continue
        deal_bas_r = exchange_data.get('deal_bas_r')        
        if deal_bas_r:
            deal_bas_r = float(deal_bas_r.replace(',', ''))
            exchange_data['deal_bas_r'] = deal_bas_r
        ttb = exchange_data.get('ttb')        
        if ttb:
            ttb = float(ttb.replace(',', ''))
            if ttb == 0.0:  # ttb가 0.0인 경우 데이터를 저장하지 않고 continue로 다음 루프로 넘어갑니다.
                continue
            exchange_data['ttb'] = ttb
        tts = exchange_data.get('tts')        
        if tts:
            tts = float(tts.replace(',', ''))
            if tts == 0.0:  # tts가 0.0인 경우 데이터를 저장하지 않고 continue로 다음 루프로 넘어갑니다.
                continue
            exchange_data['tts'] = tts
        serializer = ExchangeListSerializer(data = exchange_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            valid_res.append(exchange_data)  # 데이터가 성공적으로 저장되었다면 valid_res 리스트에 추가합니다.

    return Response(valid_res, status=status.HTTP_200_OK)  # valid_res 리스트를 반환합니다.



@api_view(['GET'])  # 예금상품 추천 알고리즘
def deposit_recomend(request):
    manibank = get_object_or_404(User, pk=request.user.pk).maninbank
    savestyle = get_object_or_404(User, pk=request.user.pk).savestyle
    
    mainbanklist = DepositBaseList.objects.filter(kor_co_nm=manibank)
    mainbank_datas = []
    all_mainbank_datas = []
    for mainbank in mainbanklist:
        all_mainbank_datas.append(mainbank)
        saveoptions = mainbank.depositoptionlist_set.filter(save_trm=savestyle)
        if saveoptions:
            mainbank_datas.append(mainbank)
    if mainbank_datas:
        serializer = DepositBaseListSerializer(data=mainbank_datas, many=True)
    else:
        serializer = DepositBaseListSerializer(data=all_mainbank_datas, many=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])  # 적금상품 추천 알고리즘
def save_recomend(request):
    manibank = get_object_or_404(User, pk=request.user.pk).maninbank
    savestyle = get_object_or_404(User, pk=request.user.pk).savestyle
    mainbanklist = SaveBaseList.objects.filter(kor_co_nm=manibank)

    mainbank_datas = []
    all_mainbank_datas = []
    for mainbank in mainbanklist:
        all_mainbank_datas.append(mainbank)
        saveoptions = mainbank.saveoptionlist_set.filter(save_trm=savestyle)
        if saveoptions:
            mainbank_datas.append(mainbank)
    if mainbank_datas:
        serializer = SaveBaseListSerializer(data=mainbank_datas, many=True)
    else:
        serializer = SaveBaseListSerializer(data=all_mainbank_datas, many=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def deposit_join(request, deposit_pk):
    product_cd = DepositBaseList.objects.get(pk=deposit_pk).fin_prdt_cd
    user = User.objects.get(pk=request.user.pk)
    # print(user.financial_products)
    # print(product_cd)
    # if User.objects.filter(financial_products__contains=product_cd).exists():
    if product_cd in user.financial_products:
        user.financial_products = user.financial_products.replace('#' + product_cd, '')
        user.save()
        return Response({'financial_products': user.financial_products })
    else:
        if user.financial_products is None:
            user.financial_products = '#' + product_cd  # 초기값 설정
        else:
            user.financial_products += '#' + product_cd  # 기존 값에 추가
        user.save()
        return Response({'financial_products': user.financial_products})
    

@api_view(['GET'])
def save_join(request, save_pk):
    product_cd = SaveBaseList.objects.get(pk=save_pk).fin_prdt_cd
    user = User.objects.get(pk=request.user.pk)
    # print(user.financial_products)
    # print(product_cd)
    # if User.objects.filter(financial_products__contains=product_cd).exists():
    if product_cd in user.financial_products:
        user.financial_products = user.financial_products.replace('#' + product_cd, '')
        user.save()
        return Response({'financial_products': user.financial_products})
    else:
        if user.financial_products is None:
            user.financial_products = '#' + product_cd  # 초기값 설정
        else:
            user.financial_products += '#' + product_cd  # 기존 값에 추가
        user.save()
        return Response({'financial_products': user.financial_products})


@api_view(['GET'])
def get_user_products(request):
    user = User.objects.get(pk=request.user.pk)
    product_codes = user.financial_products.split('#')
    results = []
    
    for code in product_codes:
        if code:  # Empty string을 건너뛰기 위한 체크
            product = DepositBaseList.objects.filter(fin_prdt_cd=code).first()
            if product:
                # results.append(model_to_dict(product))  # QuerySet -> dictionary 변환
                serializer = DepositBaseListSerializer(product)
                results.append(serializer.data)
            if not product:
                product = SaveBaseList.objects.filter(fin_prdt_cd=code).first()
                serializer = SaveBaseListDetailSerializer(product)
                results.append(serializer.data)
    
    return Response(results)