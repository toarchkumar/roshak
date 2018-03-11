'''
<a href="http://www.movable-ink-9009.com/p/cp/9faae37c33afff1b/c?mi_u=<%= INDIVIDUAL.UPLAY_ID %>&url=http%3A%2F%2Fwww.movable-ink-9009.com%2Fp%2Frp%2F8e55bdc6d1e5fbf6%2Furl" style="display: block;"><img alt="Display images to show real-time content" style="border: 0; display: block;" border="0" src="http://www.movable-ink-9009.com/p/rp/8e55bdc6d1e5fbf6.png?mi_u=<%= INDIVIDUAL.UPLAY_ID %>" /></a>

<a href="http://www.movable-ink-9009.com/p/cp/9faae37c33afff1b/c?mi_u=<%= INDIVIDUAL.UPLAY_ID %>&url=http%3A%2F%2Fwww.movable-ink-9009.com%2Fp%2Frp%2F915836c7443e599a%2Furl" style="display: block;"><img alt="Display images to show real-time content" style="border: 0; display: block;" border="0" src="http://www.movable-ink-9009.com/p/rp/915836c7443e599a.png?mi_u=<%= INDIVIDUAL.UPLAY_ID %>" /></a>
'''
# import main stuff:
import sqlalchemy as sq
import pandas as pd
import numpy as np
import boto3
import io
# import specific stuff:
from urllib import request
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

# numpy divide by zero ignore:
np.seterr(divide='ignore', invalid='ignore')

# update rds from s3:
def update_from_s3():
    engine = sq.create_engine('postgresql://toarchkumar:4gb9003k@roshakdev.cpfpv5mxcvkq.us-east-2.rds.amazonaws.com:5432/roshakdev', convert_unicode=True)
    s3 = boto3.resource('s3')
    get_data = s3.Bucket('roshak')
    master_data = pd.DataFrame()

    objects = get_data.objects.filter(Prefix='static/canvas/crm3558/data')
    for obj in objects:
        data = obj.get()['Body']
        data = io.BytesIO(data.read())
        data = pd.read_csv(data)
        master_data = master_data.append(data, ignore_index=True)
        obj.delete()
    
    master_data.to_sql('vote_campaigns', engine, if_exists='append', index=False)


# rds query function:
def get_vote_count(game):
    engine = sq.create_engine('postgresql://toarchkumar:4gb9003k@roshakdev.cpfpv5mxcvkq.us-east-2.rds.amazonaws.com:5432/roshakdev', convert_unicode=True)
    query = f"""select count(uplayid) as votes from vote_campaigns where vote = '{game}'"""

    get = pd.read_sql(query, engine)

    return float(get['votes'])

def get_total_vote_count():
    engine = sq.create_engine('postgresql://toarchkumar:4gb9003k@roshakdev.cpfpv5mxcvkq.us-east-2.rds.amazonaws.com:5432/roshakdev', convert_unicode=True)
    query = f"""select count(uplayid) as votes from vote_campaigns"""

    get = pd.read_sql(query, engine)

    return float(get['votes'])

# ac vote count image:
def inkbolt_ac():
    # params:
    get_votes = get_vote_count('ac')
    get_total_votes = get_total_vote_count()
    percentage = np.divide(get_votes, get_total_votes)

    if np.isnan(percentage):
        percentage = 0

    # image settings
    s3 = boto3.resource('s3')
    input_image = request.urlopen('https://s3.us-east-2.amazonaws.com/roshak/static/canvas/vote/ac.png')
    output = s3.Bucket('roshak')

    with Image() as image:
        with Drawing() as draw:
            draw.font = "OpenSans.otf"
            draw.font_size = 22
            draw.text_alignment = "center"
            draw.text_antialias = True

            try:
                with Image(file=input_image) as img:
                    x = int(img.width * 0.6)
                    y = int(img.height * 0.995)

                    # draw progress bar:
                    draw.fill_color=Color('#a11701')
                    draw.rectangle(left=img.width*0.11, top=img.height*0.9, width=177*percentage, height=img.height*0.2)
                    draw.draw(img)

                    # write text percentage:
                    percentage = percentage * 100
                    percentage = np.around(percentage, decimals=2)
                    draw.fill_color=Color('black')
                    draw.text(x, y, f'{percentage}%')
                    draw.draw(img)
                    
                    image.sequence.append(img)
            finally:
                input_image.close()

        image.format = 'png'
        image = image.make_blob()
        output.put_object(Key=f'static/canvas/crm3558/output/ac.png', Body=image, CacheControl='no-store, max-age=0', ContentType='image/png', ACL='public-read')

# wd2 vote count image:
def inkbolt_wd2():
    # params:
    get_votes = get_vote_count('wd2')
    get_total_votes = get_total_vote_count()
    percentage = np.divide(get_votes, get_total_votes)

    if np.isnan(percentage):
        percentage = 0

    # image settings
    s3 = boto3.resource('s3')
    input_image = request.urlopen('https://s3.us-east-2.amazonaws.com/roshak/static/canvas/vote/wd2.png')
    output = s3.Bucket('roshak')

    with Image() as image:
        with Drawing() as draw:
            draw.font = "OpenSans.otf"
            draw.font_size = 22
            draw.text_alignment = "center"
            draw.text_antialias = True

            try:
                with Image(file=input_image) as img:
                    x = int(img.width * 0.5)
                    y = int(img.height * 0.995)

                    # draw progress bar:
                    draw.fill_color=Color('#c7c7c7')
                    draw.rectangle(left=img.width*0.05, top=img.height*0.9, width=177*percentage, height=img.height*0.2)
                    draw.draw(img)

                    # write text percentage:
                    percentage = percentage * 100
                    percentage = np.around(percentage, decimals=2)
                    draw.fill_color=Color('black')
                    draw.text(x, y, f'{percentage}%')
                    draw.draw(img)
                    
                    image.sequence.append(img)
            finally:
                input_image.close()

        image.format = 'png'
        image = image.make_blob()
        output.put_object(Key=f'static/canvas/crm3558/output/wd2.png', Body=image, CacheControl='no-store, max-age=0', ContentType='image/png', ACL='public-read')

# fh vote count image:
def inkbolt_fh():
    # params:
    get_votes = get_vote_count('fh')
    get_total_votes = get_total_vote_count()
    percentage = np.divide(get_votes, get_total_votes)

    if np.isnan(percentage):
        percentage = 0

    # image settings
    s3 = boto3.resource('s3')
    input_image = request.urlopen('https://s3.us-east-2.amazonaws.com/roshak/static/canvas/vote/fh.png')
    output = s3.Bucket('roshak')

    with Image() as image:
        with Drawing() as draw:
            draw.font = "OpenSans.otf"
            draw.font_size = 22
            draw.text_alignment = "center"
            draw.text_antialias = True

            try:
                with Image(file=input_image) as img:
                    x = int(img.width * 0.5)
                    y = int(img.height * 0.995)

                    # draw progress bar:
                    draw.fill_color=Color('#1d2366')
                    draw.rectangle(left=0, top=img.height*0.9, width=177*percentage, height=img.height*0.2)
                    draw.draw(img)

                    # write text percentage:
                    percentage = percentage * 100
                    percentage = np.around(percentage, decimals=2)
                    draw.fill_color=Color('black')
                    draw.text(x, y, f'{percentage}%')
                    draw.draw(img)
                    
                    image.sequence.append(img)
            finally:
                input_image.close()

        image.format = 'png'
        image = image.make_blob()
        output.put_object(Key=f'static/canvas/crm3558/output/fh.png', Body=image, CacheControl='no-store, max-age=0', ContentType='image/png', ACL='public-read')