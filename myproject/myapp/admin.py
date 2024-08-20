import logging
from django.contrib import admin
from .models import User, Referral, Product, Application, Post, Like, Comment, Withdrawal

logger = logging.getLogger(__name__)

def process_withdrawal(withdrawal):
    if not withdrawal.is_processed:
        logger.info(f'Starting processing of withdrawal ID {withdrawal.id} for user {withdrawal.user.username}')
        withdrawal.is_processed = True
        withdrawal.save()  # Update the withdrawal to processed
        logger.info(f'Withdrawal ID {withdrawal.id} marked as processed')

        # Deduct points only when the withdrawal is processed
        withdrawal.user.points -= withdrawal.points
        withdrawal.user.save()  # Save the user to persist the new points total
        logger.info(f'Deducted {withdrawal.points} points from user {withdrawal.user.username}, new point balance: {withdrawal.user.points}')

@admin.action(description='Mark selected withdrawals as processed')
def make_processed(modeladmin, request, queryset):
    for withdrawal in queryset:
        process_withdrawal(withdrawal)

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'money_amount', 'created_at', 'is_processed')
    actions = [make_processed]

# Register your models
admin.site.register(User)
admin.site.register(Referral)
admin.site.register(Product)
admin.site.register(Application)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Withdrawal, WithdrawalAdmin)
