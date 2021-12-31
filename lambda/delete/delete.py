import boto3, os, json, uuid

client = boto3.client("dynamodb")


def main(event, context):
    print(event)
    table_name = os.environ.get("TABLE_NAME")

    id = event["id"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.delete_item(Key={"id": id})

    return {"statusCode": 200, "body": f"book deleted: {id}"}
