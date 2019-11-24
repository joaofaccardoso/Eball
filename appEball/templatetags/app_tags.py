from django import template
from appEball.models import Notification, CustomUser

register = template.Library()

@register.filter
def get_seen(value, arg):
    counter = 0
    notifications = Notification.objects.filter(user=value)
    for elem in notifications:
        if elem.isSeen == arg:
            counter+=1
    return counter

@register.filter
def getNonAcceptedUsers(value, arg):
    nonAccepetdUsers = CustomUser.objects.filter(isAccepted = arg).count()
    return nonAccepetdUsers