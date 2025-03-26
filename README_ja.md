# dicom-proxy

DICOM DIMSE プロキシサービス

## サポートするDIMSEサービス

- C-Echo
- C-Find
- C-Move

## 特徴

- シンプルで使いやすい
- Dockerデプロイ対応
- マルチクライアント設定
- デバッグログ切り替え

## 使用シナリオ

1つのAE（病院PACSなど）しかないが複数アプリケーションからアクセスが必要な場合：
- 中間プロキシとして複数クライアントからのリクエストを受信
- 上流PACSシステムへ一元的に転送
- 各クライアントのAEタイトルとネットワーク設定を管理

## 実行方法

### 方法1: ソースから実行
1. リポジトリをクローンしディレクトリへ移動:
```bash
git clone git@github.com:mario-huang/dicom-proxy.git
cd dicom-proxy
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

3. サービスを起動:
```bash
python src/main.py
```

### 方法2: Dockerデプロイ
```bash
docker compose up -d
```

## 設定

config.jsonを編集:

```json
{
    // デバッグログを有効化
    "debug": true,
    
    // プロキシサーバ設定
    "proxy": {
        "aet": "DicomProxy",     // プロキシAEタイトル
        "address": "0.0.0.0",    // リスンアドレス
        "port": 11112            // リスンポート
    },
    
    // 上流PACS設定
    "server": {
        "aet": "UpstreamPacs",   // PACS AEタイトル
        "address": "192.168.1.1",// PACS IPアドレス
        "port": 4242             // PACSポート
    },
    
    // クライアント設定リスト
    "clients": [
        {
            "aet": "ClientAET",  // クライアントAEタイトル
            "address": "192.168.1.2", // クライアントIP
            "port": 6000         // クライアントポート
        }
    ]
}
```

## 重要事項
1. ファイアウォールでプロキシポート（デフォルト11112）を開放
2. クライアント設定は各アプリケーションのDICOM設定と一致させる必要あり
3. 本番環境ではデバッグモードを無効化推奨
