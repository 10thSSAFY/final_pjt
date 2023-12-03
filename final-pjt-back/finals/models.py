from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.TextField()


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DepositBaseList(models.Model):  # 기본정보
    dcls_month = models.TextField(null=True)                # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField(null=True)                 # 금융회사 코드
    fin_prdt_cd = models.TextField(unique=True, null=True)  # 금융상품 코드
    kor_co_nm = models.TextField(null=True)                 # 금융회사 명
    fin_prdt_nm = models.TextField(null=True)               # 금융 상품명
    join_way = models.TextField(null=True)                  # 가입 방법
    mtrt_int = models.TextField(null=True)                  # 만기 후 이자율
    spcl_cnd = models.TextField(null=True)                  # 우대조건
    join_deny = models.IntegerField(null=True)              # 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField(null=True)               # 가입대상
    etc_note = models.TextField(null=True)                  # 기타 유의사항
    max_limit = models.IntegerField(null=True)              # 최고한도
    dcls_strt_day = models.TextField(null=True)             # 공시 시작일
    dcls_end_day = models.TextField(null=True)              # 공시 종료일
    fin_co_subm_day = models.TextField(null=True)           # 금융회사 제출일 [YYYYMMDDHH24MI]


class DepositOptionList(models.Model):  # 옵션정보
    baselist = models.ForeignKey(DepositBaseList, on_delete=models.CASCADE)
    intr_rate_type = models.TextField(null=True)    # 저축 금리 유형
    intr_rate_type_nm = models.TextField(null=True) # 저축 금리 유형명
    save_trm = models.IntegerField(null=True)       # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True)        # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)       # 최고 우대금리 [소수점 2자리]


class SaveBaseList(models.Model):  # 기본정보
    dcls_month = models.TextField(null=True)                # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField(null=True)                 # 금융회사 코드
    fin_prdt_cd = models.TextField(unique=True, null=True)  # 금융상품 코드
    kor_co_nm = models.TextField(null=True)                 # 금융회사 명
    fin_prdt_nm = models.TextField(null=True)               # 금융 상품명
    join_way = models.TextField(null=True)                  # 가입 방법
    mtrt_int = models.TextField(null=True)                  # 만기 후 이자율
    spcl_cnd = models.TextField(null=True)                  # 우대조건
    join_deny = models.IntegerField(null=True)              # 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField(null=True)               # 가입대상
    etc_note = models.TextField(null=True)                  # 기타 유의사항
    max_limit = models.IntegerField(null=True)              # 최고한도
    dcls_strt_day = models.TextField(null=True)             # 공시 시작일
    dcls_end_day = models.TextField(null=True)              # 공시 종료일
    fin_co_subm_day = models.TextField(null=True)           # 금융회사 제출일 [YYYYMMDDHH24MI]


class SaveOptionList(models.Model):  # 옵션정보
    baselist = models.ForeignKey(SaveBaseList, on_delete=models.CASCADE)
    intr_rate_type = models.TextField(null=True)        # 저축 금리 유형
    intr_rate_type_nm = models.TextField(null=True)     # 저축 금리 유형명
    rsrv_type = models.TextField(null=True)             # 적립 유형
    rsrv_type_nm = models.TextField(null=True)          # 적립 유형명
    save_trm = models.IntegerField(null=True)           # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True)            # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)           # 최고 우대금리 [소수점 2자리]


class ExchangeList(models.Model):
    result = models.IntegerField()      # 조회 결과
    cur_unit = models.TextField()       # 통화코드
    ttb = models.TextField()            # 전신환(송금) 받으실때
    tts = models.TextField()            # 전신환(송금) 보내실때
    deal_bas_r = models.TextField()     # 매매 기준율
    bkpr = models.TextField()           # 장부가격
    yy_efee_r = models.TextField()      # 년환가료율
    ten_dd_efee_r = models.TextField()  # 10일환가료율
    kftc_bkpr = models.TextField()      # 서울외국환중개 장부가격
    kftc_deal_bas_r = models.TextField()# 서울외국환중개 매매기준율
    cur_nm = models.TextField()         # 국가/통화명