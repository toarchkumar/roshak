import flask as f

app = f.Flask(__name__)

# import all the sub-apps:
from canvas.vote.views import mod

# blueprint registrations
app.register_blueprint(vote.views.mod, url_prefix='/vote')