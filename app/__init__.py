from flask import Flask
from flask_cors import CORS  # 添加这行
from .meetingInfo import meetingInfo_routes


def create_app():
    app = Flask(__name__)

    # 启用 CORS，允许所有域名访问 API
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    from .routes import main_routes
    app.register_blueprint(main_routes)

    from .backendRoutes import meeting_bp
    app.register_blueprint(meeting_bp, url_prefix='/api/meeting')
    app.register_blueprint(meetingInfo_routes)

    return app