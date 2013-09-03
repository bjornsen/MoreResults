from pyramid.response import Response
from pyramid.view import view_config
import requests

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='myroute')
def my_route_view(request):
    one = request.matchdict['one']
    two = request.matchdict['two']
    return Response(one + ' ' + two)

@view_config(route_name='git_autoupdate', 
             request_param='arn:aws:sns:us-west-2:934680412194:more-results-update')
def git_update(request):
    if request.matchdict['x-amz-sns-message-type'] == 'SubscriptionConfirmation':
        json = request.json_body
        url = json['SubscribeURL']
        response = requests.get(url)
        print response
        

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'MoreResults'}

    

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MoreResults_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
