import flask as f

app = f.Flask(__name__)

# import all the sub-apps:
from canvas.crm3558.views import crm3558

# blueprint registrations
app.register_blueprint(crm3558, url_prefix='/crm3558')