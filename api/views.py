from rest_framework.decorators import api_view, authentication_classes, permission_classes  # 必要なデコレーターをインポート
from sklearn.linear_model import LinearRegression  # 正しいインポートを追加
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # 必要なデコレーターをインポート
from rest_framework.authentication import BasicAuthentication  # ベーシック認証をインポート
from rest_framework.permissions import IsAuthenticated  # 認証を必要とするパーミッションをインポート
import yfinance as yf  # yfinanceをインポート
import numpy as np  # numpyをインポート

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
@authentication_classes([BasicAuthentication])  # ベーシック認証を追加
@permission_classes([IsAuthenticated])  # 認証を必要とするパーミッションを追加
# 株価データを取得
def stock_price(request):
    # クエリパラメーターから値を取得
    symbol = request.query_params.get('symbol', 'AAPL')  # デフォルト値を設定
    start = request.query_params.get('start', '2023-01-01') # デフォルト値を設定
    end = request.query_params.get('end', '2023-12-31') # デフォルト値を設定

    # 株価データを取得
    stock_data = yf.download(symbol, start=start, end=end)
    
    # データをJSON形式で返す（インデックスを文字列に変換）
    return Response(stock_data.reset_index().to_dict(orient='records'))  # DataFrameを辞書に変換して返す

@api_view(['GET'])
# 株価予測 線形回帰
def predict_stock_price(request):
    symbol = request.query_params.get('symbol', 'AAPL')  # デフォルト値を設定
    start = request.query_params.get('start', '2023-01-01') # デフォルト値を設定
    end = request.query_params.get('end', '2023-12-31') # デフォルト値を設定
    # 株価データを取得
    stock_data = yf.download(symbol, start=start, end=end)  # デフォルトの期間を設定
    if stock_data.empty:
        return Response({'error': 'Stock not found'}, status=404)  # 株が見つからない場合のエラーレスポンス

    # 予測モデル
    prices = stock_data['Close'].values.reshape(-1, 1)  # 終値を使用
    model = LinearRegression()  # 線形回帰モデルのインスタンスを作成
    model.fit(np.arange(len(prices)).reshape(-1, 1), prices)  # モデルをデータにフィットさせる

    # 予測する日数
    future_days = [1, 7, 14, 21, 30, 90, 180, 365]  # 予測する日数のリスト
    predictions = {}  # 予測結果を格納する辞書

    for days in future_days:
        next_price = model.predict(np.array([[len(prices) + days]]))  # 次の価格を予測
        predictions[f'predicted_price_{days}_days'] = next_price[0][0]  # 予測結果を辞書に追加

    return Response(predictions)  # 予測結果を返す