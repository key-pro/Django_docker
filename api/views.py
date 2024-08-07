from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # 必要なデコレーターをインポート
from rest_framework.authentication import BasicAuthentication  # ベーシック認証をインポート
from rest_framework.permissions import IsAuthenticated  # 認証を必要とするパーミッションをインポート
import yfinance as yf  # yfinanceをインポート

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
@authentication_classes([BasicAuthentication])  # ベーシック認証を追加
@permission_classes([IsAuthenticated])  # 認証を必要とするパーミッションを追加
def stock_price(request):
    # クエリパラメーターから値を取得
    symbol = request.query_params.get('symbol', 'AAPL')  # デフォルト値を設定
    start = request.query_params.get('start', '2023-01-01') # デフォルト値を設定
    end = request.query_params.get('end', '2023-12-31') # デフォルト値を設定

    # 株価データを取得
    stock_data = yf.download(symbol, start=start, end=end)
    
    # データをJSON形式で返す（インデックスを文字列に変換）
    return Response(stock_data.reset_index().to_dict(orient='records'))  # DataFrameを辞書に変換して返す



