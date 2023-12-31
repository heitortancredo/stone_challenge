"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


max_requests = 1000
worker_class = "gevent"
workers = max_workers()
