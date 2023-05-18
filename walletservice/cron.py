from userservice.models import *
from django.core.mail import send_mail
from django.conf import settings


def get_transaction_report():
    users = UserProfile.objects.all()
    user_details = {}
    for user in users.prefetch_related("wallets"):
        for wallet in user.wallets.all():
            if user_details.get(user.id) is None:
                user_details[user.id] = [{wallet.id: wallet.closing_balance}]
            else:
                user_details[user.id].append(
                    {wallet.id: wallet.closing_balance})

    send_mail(
        "Subject here",
        "user_details",
        settings.EMAIL_HOST_USER,
        ["sandeeprajsaimon999@gmail.com"],
        fail_silently=False,
        auth_user="sandysaimon1997@gmail.com",
        auth_password="Sandeep@1997"
    )
