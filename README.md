# Technical Lesson: Flask Cookies and Sessions

## Scenario

You’re working as a junior backend engineer at a tech startup that just launched
its first internal dashboard. Your team needs to track basic user interactions like
page visits and store lightweight, non-sensitive data on the client-side to
personalize experiences. Additionally, you want to persist some session information
across different routes without storing it in a database.

The product manager has asked for a demonstration app that shows:
* How data can persist across multiple requests from the same client.
* How you can update session values based on user behavior.
* How cookies behave when manually set or edited via browser dev tools.

Since cookies are such an important part of most web applications, Flask has
excellent support for cookies and sessions baked in. To test these out, let's
make a simple API to display our cookie and session data.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-cookies-and-sessions-technical-lesson)
- [API - Flask: class flask.session](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session)
- [Get and set cookies with Flask - pythonbasics.org](https://pythonbasics.org/flask-cookies/)
- [SameSite Cookies Explained](https://web.dev/samesite-cookies-explained/)
- [Chrome DevTools: Working With Cookies](https://developer.chrome.com/docs/devtools/storage/cookies/)

## Set Up

We've included some starter code for a Flask API application with this lesson so
you can see a basic example of working with sessions and cookies. The
configuration is already done, so we can work on inspecting sessions and cookies
in the app and see how we can interact with them in our code.

To set up and run the Flask application, run:

```console
$ pipenv install && pipenv shell
$ python server/app.py
```

## Instructions

### Task 1: Define the Problem

What are we solving?

The challenge is to implement client-side state persistence using Flask’s built-in session management
and cookie APIs. Specifically, you will:
* Set and update key-value pairs in Flask sessions, making sure they persist across multiple requests
from the same client.
* Expose dynamic API endpoints that allow users to retrieve or modify these session values.
* Use cookies to store a value that the user can manually inspect or edit, highlighting the difference
between manually-set cookies and Flask’s secure session cookie.
* Return session and cookie data in a JSON response, to give visibility into browser-client interaction.

In applications, maintaining session and cookie state is critical for tasks such as:
* Tracking logged-in users
* Saving in-progress forms or cart data
* Personalizing content delivery

Using session data allows backend developers to store user-specific data securely without needing to
create a database table for transient information. Understanding cookie behavior is equally essential
for debugging, front-end communication, and cross-site security.


You will know you’ve implemented this correctly when:
* Session values persist across refreshes and route navigation.
* The count value increments correctly per visit.
* A manually-set cookie appears in browser dev tools and the app’s JSON response.
* You understand which values are encrypted and which are readable via developer tools.

### Task 2: Determine the Design

We're going to set 3 session keys with initial values:
- hello, initial value = "World"
- goodnight, initial value = "Moon"
- count, initial value = 0

The keys can each be accessed by their individual routes:
- `http://localhost:5555/sessions/hello`
- `http://localhost:5555/sessions/goodnight`
- `http://localhost:5555/sessions/count`

The `count` session will be incremented by 1 each time
`http://localhost:5555/sessions/count` is visited.

We will also set a cookie:
- mouse, set to "Cookie"

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Initialize Session

In app.py, we'll build a dynamic route to show any of our session keys:

```python
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    pass
```

After defining the route, let's define our 3 keys and set them to the
initial value:

```python
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    session["hello"] = "World"
    session["goodnight"] = "Moon"
    session["count"] = 0
```

Typically, we want to be able to alter session data and retain that value as
a user navigates an application. Think about how when you log into an application,
it won't log you out when you refresh the page, submit a form, or navigate to
a new page.

Let's handle this with some logic to see if a value already exists before setting
the initial value.
```python
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0
```

Here, we use `.get` rather than `session[key]` to prevent an error if the key
does not yet exist.

#### Step 2: Update Session

Next, we need to handle updating the count session key everytime the 
`/sessions/count` route is visited.

```python
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0

    if key == "count":
        session["count"] += 1
```

#### Step 3: Send Response

Finally, we can use our session object in the response:

```python
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0

    if key == "count":
        session["count"] += 1

    response = make_response(jsonify({
        'session': {
            'session_key': key,
            'session_value': session[key],
            'session_accessed': session.accessed,
        },
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
    }), 200)

    return response
```

In this response, we're sending info based on the session we set.

We're also displaying all cookies. We're not currently manually setting any cookies,
but since we have a session, the entire session object will be stored in that cookie
in an encrypted format.

#### Step 4: Set Cookie on Response

Next, let's set a cookie. We'll create a route `/crumbs`:

```python
@app.route('/crumbs', methods=['GET'])
def follow_crumbs():
    pass
```

Next, to set a cookie, we need to create our response. Let's show all cookies
again and include a message:

```python
@app.route('/crumbs', methods=['GET'])
def follow_crumbs():
    response = make_response(jsonify({
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
        'message': 'mouse successfully followed crumbs'
    }), 200)

    return response
```

Finally, we can set our cookie:

```python
@app.route('/crumbs', methods=['GET'])
def follow_crumbs():
    response = make_response(jsonify({
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
        'message': 'mouse successfully followed crumbs'
    }), 200)

    response.set_cookie('mouse', 'Cookie')

    return response
```

#### Step 5: Test and Review Final Code

In the browser, make a request to `http://localhost:5555/sessions/hello`.
This will run the code in our `show_session()` view function:

```py
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):

    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"
    session["count"] = session.get("count") or 0

    if key == "count":
        session["count"] += 1

    response = make_response(jsonify({
        'session': {
            'session_key': key,
            'session_value': session[key],
            'session_accessed': session.accessed,
        },
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
    }), 200)

    return response
```

In this function, we're setting values on the `session` object and serializing
in the response so we can view their values in the browser.

Note that we are using a ternary operator to set values for our session; we
typically want our session to stay consistent until a user ends it, so we only
set certain values if they do not already exist.

Next, make a request to `http://localhost:5555/crumbs`.
This will run the code in our `follow_crumbs()` view function:

```python
@app.route('/crumbs', methods=['GET'])
def follow_crumbs():
    response = make_response(jsonify({
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
        'message': 'mouse successfully followed crumbs'
    }), 200)

    response.set_cookie('mouse', 'Cookie')

    return response
```

The first time a user makes a request to this endpoint, Flask will include the
`Set-Cookie` **response header** with our sessions and cookies values, which
will instruct the browser to store these values in memory and send them with any
future requests on this domain.

![set-cookie headers](/assets/python-p4-cookies-in-flask-api-1.png)

After making the request, navigate to `http://localhost:5555/sessions/hello` again.
You should see something like this in the browser:

```json
{
  "cookies": [
    {
      "mouse": "Cookie"
    },
    {
      "session": "eyJnb29kbmlnaHQiOiJNb29uIiwiaGVsbG8iOiJXb3JsZCJ9.Y3KXKQ.oTqGI6rmhKDNLizZaHfJadRybUc"
    }
  ],
  "session": {
    "session_accessed": true,
    "session_key": "hello",
    "session_value": "World"
  }
}
```

From this, we can see that the session and cookies objects can both be used to
store key-value pairs of data. The entire session object is actually stored in
that `session` cookie, in a signed and encrypted format, which makes it
impossible for users to tamper with.

You can view cookie information directly in the browser as well. In the
developer tools, find the **Application** tab, and go to the **Cookies** section
(under "Storage" in the pane on the left). There, you'll find all the cookies
for our domain (`http://localhost:5555`):

![cookies in dev tools](/assets/python-p4-cookies-in-flask-api-2.png)

Cookies can be edited directly in the dev tools. Try changing the value of the
`mouse` key to something new. Then refresh the page in the browser to
make another request. If you try to edit the `session` cookie, on the other
hand, it will have no effect thanks to Flask security features like signing and
encryption.

Feel free to test the other routes, clearing cookies every now and then to see 
how the cookies and sessions are set.

#### Step 6: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Conclusion

Cookies are an integral part of modern web applications; they help keep track of
**stateful** information in an inherently **stateless** protocol by
automatically passing additional data with each request using the headers. We
can get a better sense of how cookies are being used by websites using the
browser dev tools.

## Considerations

### Common pitfalls:

* Overwriting session data
  * Reassigning values directly without checking if they exist (session['key'] = 'value') can erase prior data.
  * Always use .get() or conditional logic.
* Route-specific logic
  * Our current application route logic doesn’t handle edge cases (e.g., a missing key). Currently, the app throw errors, so in production applications we would include more error handling.
* Browser caching and cookie updates
  * Cookies may not update immediately if the browser caches aggressively; dev tools should be used in real time.
* Misconception about cookie security
  * Not all cookies are encrypted. In this example, only the Flask session cookie is signed/encrypted.
    * Session data is stored in the cookie, but Flask handles encryption/decryption.
  * Be very careful whenever using or sending sensitive information to the frontend.