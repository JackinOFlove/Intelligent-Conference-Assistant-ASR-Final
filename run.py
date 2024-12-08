# 在这里导入 create_app 函数
from app import create_app
from flask_cors import CORS

app = create_app()

# 开发环境下允许所有跨域请求
CORS(app, supports_credentials=True)

if __name__ == "__main__":
    # 允许所有域名访问
    app.run(
        debug=True,  # 开启调试模式
        host='0.0.0.0',  # 允许所有IP访问
        port=5000,  # 指定端口
        threaded=True  # 启用多线程
    )