from documents import get_collection

def notifications(request):
    """
    Returns unread notification count
    """

    if request.user.is_anonymous():
        notification_count = 0
    else:
        notification_count = get_collection("notifications").find({
            "recipient": request.user.id,
            "is_read": False
        }).count()

    return {
        "notification_count": notification_count
    }