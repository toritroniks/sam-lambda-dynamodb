import json
import boto3
import os
import logging
from datetime import datetime

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        session = boto3.session.Session()
        awsRegion = session.region_name
        paramList = event['queryStringParameters']

        client = boto3.client('dynamodb')
        # ローカルの場合
        if os.environ['ENV'] == 'local':
            dynamodb = boto3.resource('dynamodb', region_name = awsRegion, endpoint_url = "http://dynamodb:8000")
        # ローカル以外の環境の場合
        else:
            dynamodb = boto3.resource('dynamodb', region_name = awsRegion)
        # テーブルを取得
        table = dynamodb.Table('Access')
        # 日時の文字列
        date = datetime.utcnow().isoformat()
        # 登録するアイテムのベース
        item = {'Path': event['path'], 'Date': date}

        if paramList != None:
            for key,value in paramList.items():
                item[key] = value

        table.put_item(
            Item=item
        )

    except Exception as e:
        # Lambdaログにエクセプションの情報を入れる
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error_message': str(e)
            }),
        }
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
