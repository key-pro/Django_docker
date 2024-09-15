from django.urls import path
from .views import hello_world, stock_price, predict_stock_price

urlpatterns = [
  path('hello-world/', hello_world),
  path('stock_price/', stock_price),
  path('predict_stock_price/',predict_stock_price),
  # path('predict_stock_price_tf/',predict_stock_price_tf),
]