# 環境構築

## 前提条件
- Dockerがインストールされている
- VSCodeがインストールされている
- Python3.7がインストールされている

## バージョン確認
- python3.7はインストールされていることを確認

```
sam-lambda-dynamodb> python -V
Python 3.7.2
```
- pipを更新する

```
sam-lambda-dynamodb> python -m pip install --upgrade pip
```

## 仮想環境作成
自分のローカル環境のライブラリーのバージョンなどが影響しないように仮想環境を作ります。

- 仮想環境をvenvライブラリーで作成し、activateする

```
sam-lambda-dynamodb> python -m venv venv
sam-lambda-dynamodb> .\venv\Scripts\activate
(venv) sam-lambda-dynamodb>
```
- 仮想環境の中のpipも更新

```
(venv) sam-lambda-dynamodb> python -m pip install --upgrade pip
```
activateスクリプトを実行できない場合:
- 管理者として以下のコマンドを実行する

```
set-executionpolicy remotesigned
```

仮想環境のための設定を入れます。
- VSCODEに「Python」というExtensionをインストールします。
- 「F1」を押し、```>Preferences: Open Workspace Settings```　を書きます。
- 「Python: Python Path」の設定を探し、仮想環境のpython.exeのパスを入力します。
	- 例：```C:\\Users\\path\\to\\sam-lambda-dynamodb\\venv\\Scripts\\python.exe```
- 「Python: Venv Path」の設定を探し、仮想環境のベースパスを入力します。
  - 例：```C:\\Users\\path\\to\\sam-lambda-dynamodb\\venv```
- 設定終わると、ワークスペースフォルダーに```.vscode/settings.json```が自動的に作成されます。
	- ```settings.json```の中身は以下のようになります。

```json:settings.json
{
	"python.pythonPath": "C:\\Users\\path\\to\\sam-lambda-dynamodb\\venv\\Scripts\\python.exe",
	"python.venvPath": "C:\\Users\\path\\to\\sam-lambda-dynamodb\\venv"
}
```

## 仮想環境に必要なライブラリーをインストール
- ```requirements.txt```にすべての必要なライブラリーが書いてあるので、インストールするため以下のコマンドを実行します。

```
(venv) sam-lambda-dynamodb> pip install -r requirements.txt
```

## ローカルのawsの設定
- ```aws configure```コマンドで以下のように設定します。

```
(venv) sam-lambda-dynamodb> aws configure
AWS Access Key ID: testid
AWS Secret Access Key: testkey
Default region name: ap-northeast-1
Default output format: json
```

## DynamoDBの設定
- Containerをダウンロードする

```
(venv) sam-lambda-dynamodb> docker pull amazon/dynamodb-local
```
- Dockerのネットワークを作成する
```
(venv) sam-lambda-dynamodb> docker network create lambda-local
```

- Containerを実行する

```
(venv) sam-lambda-dynamodb> docker run --network lambda-local --name dynamodb -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb
```
- jsonからテーブルを作成する

```
(venv) sam-lambda-dynamodb> aws dynamodb create-table --cli-input-json file://.\DynamoDB\AccessTable.json --endpoint-url http://localhost:8000
```

## SAMアプリをビルドする
- ```sam-app```フォルダに移動し、ビルドコマンドを実行

```
(venv) sam-lambda-dynamodb> cd .\sam-app\
(venv) sam-lambda-dynamodb\sam-app> sam build
```
- SAMのAPIをDynamoDBと同じネットワークで開始する

```
(venv) sam-lambda-dynamodb\sam-app> sam local start-api --docker-network lambda-local
```

## テストする

ブラウザーでGatewayにアクセスします。(**http://localhost:3000/hello?param=test**)

成功できたら、以下のコマンドでテーブルのアイテムが見れます。

```
(venv) sam-lambda-dynamodb> aws dynamodb scan --table-name Access --endpoint-url http://localhost:8000
{
    "Items": [
        {
            "Path": {
                "S": "/hello"
            },
            "param": {
                "S": "test"
            },
            "Date": {
                "S": "2019-02-11T03:48:44.017178"
            }
        }
    ],
    "Count": 1,
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```