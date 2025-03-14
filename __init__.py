import os

from flask import Flask # type: ignore
from flask import session

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='LACTANTAP',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/reset')
    def reset():
        session.clear()
    
    from . import db
    db.init_app(app)
    aspec = {}
    from . import calc
    app.register_blueprint(calc.bp, aspec = aspec)



    return app