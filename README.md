What is this?
=============

The few scripts under `fs/` demonstrates a Flask / FastAPI web application forwarding user messages over a long-lived
socket to another system.
I wrote this for a friend who wanted to stop using the flask development server.

How to use
==========

There is a simple TCP server at `fs/echo.py` for the background socket to connect to. Run this one first before starting
the example scripts.

Then the following scripts demonstrates a few approaches:

  - `fs/flask_reference.py`

This is my interpretation of the system my friend currently has.
A background thread is started and the web endpoints communicate with the background worker over a `queue.Queue`

  - `fs/flask_process.py`

Very similar to above but using a background process and a `multiprocessing.Queue` instead

  - `fs/flask_gunicorn_workers.py`

Keep using a background process but introduces serving the Flask app with gunicorn instead of the Flask development
server.

- `fs/fastapi_bg.py`

A different approach leveraging asynchronous IO (using FastAPI). Note that in this approach there would be one
long-lived socket per process and no queue. This makes sense since async IO applications typically use fewer threads /
processes.