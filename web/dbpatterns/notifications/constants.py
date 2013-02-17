NOTIFICATION_TYPE_FORK = "fork"
NOTIFICATION_TYPE_COMMENT = "comment"
NOTIFICATION_TYPE_STAR = "star"
NOTIFICATION_TYPE_FOLLOWING = "following"
NOTIFICATION_TYPE_ASSIGNMENT = "assignment"

NOTIFICATION_TEMPLATES = {
    NOTIFICATION_TYPE_FORK: '%(username)s forked your document.',
    NOTIFICATION_TYPE_STAR: '%(username)s starred your document.',
    NOTIFICATION_TYPE_COMMENT: '%(username)s commented on your document.',
    NOTIFICATION_TYPE_FOLLOWING: '%(username)s is following you.',
    NOTIFICATION_TYPE_ASSIGNMENT: '%(username)s assigned you in a document.',
}