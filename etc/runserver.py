import sys, os, socket
from os.path import dirname

#This shoves the directory that bestsellers/ is sitting in on to the path
new_dir = dirname(dirname(dirname(os.path.abspath(__file__))))
sys.path.append(new_dir)
print "Adding dir to path: ",new_dir


#This shoves the pyapps directory onto the end of the path, so that we can find those apps
#This would be set in your Apache config (see ../README for Apache setup)
sys.path.append('/var/pyapps') 

from bestsellers import app as application
#from brandeis.utilities.global_config import ENV

# Don't allow the Flask Development Server outside of Dev.
#assert ENV == "dev"

# Force SANDBOX_PORT -- the Flask development server should only ever be run with a port specified.
if application.config.get('SANDBOX_PORT') is None:
    sys.exit("Can't run runserver.py without a SANDBOX_PORT defined in config_sandbox.py")

hostname = socket.gethostname()

# Print this stuff only after reloader has been set, to prevent printing twice
if 'WERKZEUG_RELOADER' in os.environ:
    if hostname == 'wmd-app-dev-rhel6.unet.brandeis.edu':
        print "You can access this sandbox app at: http://apps-dev.brandeis.edu:"+str(application.config.get('SANDBOX_PORT'))+"/"
    
    print "Valid URLS:"
    for rule in application.url_map.iter_rules():
        print "    "+rule.rule+" -> "+rule.endpoint
    
    print "DB Info: "
    print application.config.get('SQLALCHEMY_DATABASE_URI')

# Runserver always restarts with the reloader, so set this to true on first run
os.environ['WERKZEUG_RELOADER'] = 'TRUE'

ip = socket.gethostbyname(socket.getfqdn())
#application.config['DEV_SERVER'] = True
#application.run(host=ip,debug=True,port=application.config.get('SANDBOX_PORT'))
application.config['DEV_SERVER'] = False
application.run(host=ip,debug=False,port=application.config.get('SANDBOX_PORT'))
