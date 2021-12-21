import boto3, os, json, uuid

client = boto3.client('dynamodb')

def main(event, context):
    print(event)
    table_name = os.environ.get('TABLE_NAME')

    title = event["title"]
    author = event['author']

    id = str(uuid.uuid4())[0:8]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item={
        'id': id,
        'title': title,
        'author': author
    })

    return {
        'statusCode': 200,
        'body': f"book added: {title}"
    }