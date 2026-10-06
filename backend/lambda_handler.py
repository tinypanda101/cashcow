"""
Entrypoint for AWS Lambda
Mangum translates between lambda and the ASGI interface that FASTAPI uses
"""


from mangum import Mangum

from app.main import app

handler = Mangum(app)