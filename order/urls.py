from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import OrderViewSet, OrderItemsViewSet, submit_order

router = DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"orderitems", OrderItemsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "add_to_order/",
        OrderItemsViewSet.as_view({"post": "add_to_order"}),
        name="add_to_order",
    ),
    path(
        "remove_from_order/",
        OrderItemsViewSet.as_view({"post": "remove_from_order"}),
        name="remove_from_order",
    ),
    path(
        "decrease_from_order/",
        OrderItemsViewSet.as_view({"post": "decrease_from_order"}),
        name="decrease_from_order",
    ),
    path("submit_order", submit_order, name="submit_order"),
]
