from django.urls import include, path
from items import views

urlpatterns = [
    path('buy/<int:id>', views.buy_item, name='buy_item'),
    path('item/<int:id>', views.item_detail, name='item_detail'),
    path('buy_order/<int:id>', views.buy_order, name='buy_order'),
    path('order/<int:id>', views.order_detail, name='order_detail'),
    path('success',views.success ),
    path('intent/buy/<int:id>', views.buy_item_intent, name='buy_item'),
    path('intent/item/<int:id>', view=views.item_detail_intent, name='item_detail'),
    path('intent/buy_order/<int:id>', views.buy_order_intent, name='buy_order'),
    path('intent/order/<int:id>', views.order_detail_intent, name='order_detail'),
    
]
