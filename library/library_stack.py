from aws_cdk import (
    core as cdk,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway
)

from aws_cdk import core
import json


class LibraryStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create library table
        table = dynamodb.Table(self, "books-table",
                partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
                )

        # Create book post function 
        def post_book():
            post_fn = lambda_.Function(self, "post",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="post.main",
            code=lambda_.Code.from_asset("./lambda/post")
        )
            # grant reand and write permissions to the table
            table.grant_read_write_data(post_fn)
            post_fn.add_environment("TABLE_NAME", table.table_name)

            return post_fn

        
        # Create book post function 
        def get_books():
            get_fn = lambda_.Function(self, "get",
                runtime=lambda_.Runtime.PYTHON_3_7,
                handler="get.main",
                code=lambda_.Code.from_asset("./lambda/get")
            )


            table.grant_read_write_data(get_fn)
            get_fn.add_environment("TABLE_NAME", table.table_name)

            return get_fn
        
        # Create API function
        def create_api(get_fn, post_fn):
            api = apigateway.LambdaRestApi(self, "library-api", endpoint_configuration=apigateway.EndpointConfiguration(
            types=[apigateway.EndpointType.REGIONAL]),
                handler=get_fn,
                proxy=False
            )
            books = api.root.add_resource("books")
        
            post_book_integration = apigateway.LambdaIntegration(post_fn, proxy=False, integration_responses=[apigateway.IntegrationResponse(
                status_code="200")])
            get_book_integration = apigateway.LambdaIntegration(get_fn, proxy=False, integration_responses=[apigateway.IntegrationResponse(
                status_code="200"
                )])

            books.add_method("GET", get_book_integration, method_responses=[apigateway.MethodResponse(
            status_code="200"
            )]) # GET /books
            books.add_method("POST", post_book_integration, method_responses=[apigateway.MethodResponse(
            status_code="200"
            )]) 

        post_book = post_book()
        get_books = get_books()
        create_api(get_books, post_book)


# CREATE FRONT-END IN FLASK WITH SLS? https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/
# CREATE POST AND GET FUNCTIONS
# ADD LOCATION COLUMN FOR BOOKS (e.g here or at friends house)
# ADD BOOK OWNER COLUMN F or A
# ADD FILTER FOR F or A in search
# ADD COLUMN FOR BORROWED AND WHO HAS IT
# Create update book status function 

# ADD API SECURITY (API KEY? COGNITO?)
# - https://awskarthik82.medium.com/part-1-securing-aws-api-gateway-using-aws-cognito-oauth2-scopes-410e7fb4a4c0 
# - https://www.youtube.com/watch?v=4n5Ssr3NZRc

# DOMAIN NAME

# CREATE GITHUB PIPELINE





