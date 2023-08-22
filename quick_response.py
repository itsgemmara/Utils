import atexit
import queue
import threading


from django.core.mail import mail_admins


def _worker():
    while True:
        func, args, kwargs = _queue.get()
        try:
            func(*args, **kwargs)
        except:
            import traceback
            details = traceback.format_exc()
            mail_admins('Background process exception', details)
        finally:
            _queue.task_done()  # so we can join at exit

def postpone(func):
    def decorator(*args, **kwadef rgs):
        _queue.put((func, args, kwargs))
    return decorator

_queue = queue.Queue()
_thread = threading.Thread(target=_worker)
_thread.daemon = True
_thread.start()

def _cleanup():
    _queue.join()   # so we don't exit too soon

atexit.register(_cleanup)