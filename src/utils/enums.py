import enum


class RoleEnum(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class StatusEnum(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
