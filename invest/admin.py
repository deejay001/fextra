from django.contrib import admin
from .models import Coupon, Plan, Profile, Withdrawal, Wtype

# Register your models here.


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'time')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    exclude = ('code', 'output', 'expire_on')
    list_display = ('user', 'plan', 'stake', 'code', 'status', 'output', 'created_on', 'expire_on')
    list_filter = ('plan', 'status')
    search_fields = ['code']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ref_code', 'ref_num')
    search_fields = ['user']


@admin.register(Wtype)
class WtypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Withdrawal)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('name','w_type', 'cash', 'ac_name', 'ac_num', 'bank', 'status', 'created_on')
    list_filter = ('bank', 'status', 'created_on')
    search_fields = ['name', 'ac_num', 'ac_name']
