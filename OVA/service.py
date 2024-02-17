from django.core.mail import send_mail

def send(user_email):
    send_mail(
        'U are subscribed to our site',
        'We will send u useful info!',
        'OVAtaked@gmail.com',
        [user_email],
        fail_silently=False
    )