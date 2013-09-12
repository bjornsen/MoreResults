from pyramid.response import Response
from pyramid.view import view_config
import requests
import logging

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

log = logging.getLogger(__name__)


@view_config(route_name='myroute')
def my_route_view(request):
    one = request.matchdict['one']
    two = request.matchdict['two']
    return Response(one + ' ' + two)

@view_config(route_name='git_autoupdate')
def git_update(request):
    try:
        if request.matchdict['x-amz-sns-message-type'] == 'SubscriptionConfirmation':
            json = request.json_body
            url = json['SubscribeURL']
            response = requests.get(url)
            log.debut('Received Subscription Confirmation from Amazon SNS')
        elif request.matchdict['x-amz-sns-message-type'] == 'Notification':
            log.debug('Received a notification from Amazon SNS')
            return Response('OK')
    except KeyError:
        log.debug('Not an Amazon SNS notification')
        return Response('Not an Amazon SNS notification')

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

