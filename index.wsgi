import sae
from tinytrue import wsgi

application = sae.create_wsgi_app(wsgi.application)