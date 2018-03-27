# import main stuff:
import flask as f
import pandas as pd
import boto3
import datetime as dt
import gzip as gz

# flask blueprint:
crm3558 = f.Blueprint('vote', __name__, static_folder='static')

def vote_to_s3(uplayid, vote):
    timenow = dt.datetime.now()
    s3 = boto3.resource('s3')
    output = s3.Bucket('roshak')

    if vote in ['m1', 'm2', 'm3', 'm4', 'm5']:
        data = {
            'uplayid' : [uplayid],
            'vote' : [vote],
            'campaign_label' : 'PI-GRW-NCSA-E-BC-180313-3558-TU13PVP',
            'vote_datetime' : [timenow]
        }
        get = pd.DataFrame(data)
        to_save = get.to_csv(None, index=False).encode('utf-8')
        output = output.put_object(Key=f'static/canvas/crm3558/data/{uplayid}_{timenow}.csv', Body=to_save, ACL='private')
    else:
        pass

# voting logic:
@crm3558.route('/vote')
def vote():
    uplayid = f.request.args.get('uplayid')
    vote = f.request.args.get('vote')
    url = f.request.args.get('url')

    try:
        vote_to_s3(uplayid, vote)
    except:
        pass

    return f.redirect(url)