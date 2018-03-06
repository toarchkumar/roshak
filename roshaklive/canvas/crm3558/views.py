# import main stuff:
import flask as f
import sqlalchemy as sq
import pandas as pd
import boto3

# flask blueprint:
crm3558 = f.Blueprint('vote', __name__, static_folder='static')

# voting logic:
@crm3558.route('/vote')
def vote():
    engine = sq.create_engine('postgresql://toarchkumar:4gb9003k@roshakdev.cpfpv5mxcvkq.us-east-2.rds.amazonaws.com:5432/roshakdev', convert_unicode=True)
    uplayid = f.request.args.get('uplayid')
    vote = f.request.args.get('vote')
    url = f.request.args.get('url')

    data = {
        'uplayid' : [uplayid],
        'vote' : [vote]
    }
    get = pd.DataFrame(data)
    get.to_sql('users', engine, if_exists='append', index=False)

    return f.redirect(url)