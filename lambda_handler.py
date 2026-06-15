from serverless_wsgi import handle
from app.main import app

def handler(event, context):
    return handle(app, event, context)
