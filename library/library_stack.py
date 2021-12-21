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

        # The code that defines your stack goes here
        table = dynamodb.Table(self, "books-table",
                partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
                )
        
        # POST
        post_fn = lambda_.Function(self, "post",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="post.main",
            code=lambda_.Code.from_asset("./lambda/post")
        )


        table.grant_read_write_data(post_fn)
        post_fn.add_environment("TABLE_NAME", table.table_name)


        # GET
        get_fn = lambda_.Function(self, "get",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="get.main",
            code=lambda_.Code.from_asset("./lambda/get")
        )


        table.grant_read_write_data(get_fn)
        get_fn.add_environment("TABLE_NAME", table.table_name)


        # API
        api = apigateway.LambdaRestApi(self, "library-api", endpoint_configuration=apigateway.EndpointConfiguration(
        types=[apigateway.EndpointType.REGIONAL]),
            handler=get_fn,
            proxy=False
        )
        books = api.root.add_resource("books")
        
        post_book_integration = apigateway.LambdaIntegration(post_fn, proxy=False, integration_responses=[apigateway.IntegrationResponse(
            status_code="200")])
        get_book_integration = apigateway.LambdaIntegration(get_fn, proxy=False, integration_responses=[apigateway.IntegrationResponse(
            status_code="200")])

        books.add_method("GET", get_book_integration, method_responses=[apigateway.MethodResponse(
        # Successful response from the integration
        status_code="200"
    )]) # GET /books
        books.add_method("POST", post_book_integration, method_responses=[apigateway.MethodResponse(
        # Successful response from the integration
        status_code="200"
    )]) 
    # POST /books


# Test
# CREATE POST AND GET FUNCTIONS
# ADD LOCATION COLUMN FOR BOOKS (e.g here or at friends house)

# ADD API SECURITY (API KEY? COGNITO?)

# DOMAIN NAME





