from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    user: User,
    date: str | None = None
) -> Order:
    order_kwargs = {"user": user}
    if date:
        order_kwargs["created_at"] = date

    order = Order.objects.create(**order_kwargs)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
