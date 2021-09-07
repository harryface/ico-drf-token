from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bid, CustomUser, SiteConfiguration, SuccessfulBid, UnSuccessfulBid

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'password', 'email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('AlexaBitcoins Permissions', {'fields': ()}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):

    list_display = ('coin_name', 'start_date', 'end_date')

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and SiteConfiguration.objects.exists():
            retVal = False
        return retVal


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    list_display = ('user', 'number_of_tokens',
                    'bidding_price', 'unit_price', 'created_at')


@admin.register(SuccessfulBid)
class SuccessfulBidAdmin(admin.ModelAdmin):

    list_display = ('bid', 'token_allotted')

admin.register(UnSuccessfulBid)