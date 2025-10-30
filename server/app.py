from flask import Flask, request, session, jsonify, make_response

app = Flask(__name__)
app.json.compact = False

app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

# --------------------------
# Session Initialization Route
# --------------------------
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    """
    Initializes session keys for 'hello', 'goodnight', and 'count'.
    Uses .get() to preserve values if they already exist.
    Returns all current session data in a JSON response.
    """
    # Initialize each session key safely
    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0

    # Return a summary of current session state
    return jsonify({
        "message": f"Session initialized for key: {key}",
        "session": {
            "hello": session["hello"],
            "goodnight": session["goodnight"],
            "count": session["count"]
        }
    }), 200

if __name__ == '__main__':
    app.run(port=5555)
    