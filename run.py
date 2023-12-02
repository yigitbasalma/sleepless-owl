from w import app, socketio

socketio.run(app, host="127.0.0.1", port=8080, allow_unsafe_werkzeug=True)
