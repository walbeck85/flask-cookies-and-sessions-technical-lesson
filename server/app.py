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
    Initializes session keys, updates 'count' if needed,
    and returns both session and cookie data as JSON.
    """

    # Initialize session keys safely
    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0

    # Increment count when /sessions/count is visited
    if key == "count":
        session["count"] += 1

    # Build a response with detailed session + cookie info
    response = make_response(jsonify({
        "session": {
            "session_key": key,
            "session_value": session[key],
            "session_accessed": session.accessed,
        },
        "cookies": [
            {cookie: request.cookies[cookie]} for cookie in request.cookies
        ],
    }), 200)

    return response

if __name__ == '__main__':
    app.run(port=5555)
    