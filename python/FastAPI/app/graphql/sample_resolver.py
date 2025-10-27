from app.graphql.sample_schema import schema

def execute_query(query: str):
    """Executes a GraphQL query"""
    result = schema.execute(query)
    return result.data