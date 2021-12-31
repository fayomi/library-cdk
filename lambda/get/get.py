import boto3, os, json

client = boto3.client("dynamodb")


def main(event, context):
    table_name = os.environ.get("TABLE_NAME")
    response = client.scan(TableName=table_name)
    # code to get all books from table

    # print(response["Items"])
    books = []
    for item in response["Items"]:
        new_item = {"id": item["id"]["S"],  "author": item["author"]["S"], "title": item["title"]["S"]}
        books.append(new_item)

    print(books)

    return {"statusCode": 200, "body": books}
