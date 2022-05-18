#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
import logging
from logging import Formatter, FileHandler
from models import db
from routes import api


def create_app(test_config=None):
    #----------------------------------------------------------------------------#
    # App Config.
    #----------------------------------------------------------------------------#
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)
    

    #  API 
    #  ----------------------------------------------------------------
    app.register_blueprint(api, url_prefix='/api/v1')


    #  error Handler
    #  ----------------------------------------------------------------
    '''
        error handling for unprocessable entity
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
        implement error handler for 404
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
        implement error handler for AuthError 
    '''
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "This resource need authentication"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You don't have permissions to access this resources"
        }), 403

    return app

app = create_app()

"""
 Log Management
"""
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

