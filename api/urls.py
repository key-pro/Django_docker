from django.urls import path
from .views import hello_world, stock_price

urlpatterns = [
  path('hello-world/', hello_world),
  path('stock_price/', stock_price),
]