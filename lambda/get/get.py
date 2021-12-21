import boto3, os, json

client = boto3.client('dynamodb')

def main(event, context):
    table_name = os.environ.get('TABLE_NAME')
    response = client.scan(TableName=table_name)
    # code to get all books from table
    
    # print(response["Items"])
    books = []
    for item in response["Items"]:
        books.append(item["author"]["S"] + ": " + item["title"]["S"])
    
    print(books)

    return {
        'statusCode': 200,
        'body': books
    }