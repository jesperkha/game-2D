# Version 1.0
# Event handler

from config import FPS, append_loop

_queue = []
_timeouts = []
_event_listeners = []
_timed_event_listeners = []
_ticks = 0
_seconds = 0

def time_elapsed_seconds() -> int:
    "Returns the time elapsed in seconds since start"
    return _seconds


def time_elapsed_ticks() -> int:
    "Returns the total number of frames since start"
    return _ticks


def push_timed_event(time_seconds: int, callback, interval: bool = False) -> None:
    """
    - param1 `int`: Time to event call in seconds
    - param2 `function`: Callback method for event call
    - param3 `bool`: True if event should keep running after first call.
    """
    _timed_event_listeners.append([time_seconds, _ticks + time_seconds * FPS, callback, interval])


def get_event(event: int) -> bool:
    """
    - param `int`: Event constant
    - returns `bool`: If event is queued.
    """
    for e in _queue:
        if e[0] == event: return True
    
    return False


def push_event(event: int, stay: bool = False) -> bool:
    """
    - param1 `int`: Event constant
    - param2 `bool`: True if event should stay after new frame call
    - returns `bool`: If an event was added or not. False if event was already queued.
    """
    if get_event(event):
        return False

    _queue.append((event, stay))
    return True


def pop_event(event: int) -> bool:
    """
    - param `int`: Event constant
    - returns `bool`: If an event was removed or not. False if event was not queued.
    """
    if get_event(event):
        for e in _queue:
            if e[0] == event: _queue.remove(e)
        return True
    
    return False


def push_event_listener(event: int, callback) -> bool:
    """
    Replaces existing listener for same event.
    - param1 `int`: Event constant
    - param2 `function`: Callback for when event is queued.
    - returns `bool`: If a listener was replaced.
    """
    is_exist = False

    for listener in _event_listeners:
        if listener[0] == event:
            _event_listeners.remove(listener)
            is_exist = True
            break

    _event_listeners.append((event, callback))
    return is_exist


def pop_event_listener(event: int) -> bool:
    """
    - param `int`: Event constant
    - returns `bool`: If a listener was removed.
    """
    for listener in _event_listeners:
        if listener[0] == event:
            _event_listeners.remove(listener)
            return True
    
    return False


def set_timeout(frames: int, callback) -> None:
    """
    Queues new timeout event. Calls callback after n frames.
    - param1 `int`: Number of frames before callback
    - param2 `function`: Callback function (0 args)
    """
    _timeouts.append([frames, callback])


def update_all(win, dt) -> None:
    """
    Calls event listeners and removes all queued events after.
    Can be called at beginning or end of main loop. End is recommended.
    """
    global _ticks, _seconds
    _ticks += 1
    if _ticks % FPS == 0:
        _seconds += 1

    for listener in _event_listeners:
        if get_event(listener[0]): listener[1]()

    for listener in _timed_event_listeners:
        if _ticks == listener[1]:
            listener[2]()
            listener[1] = _ticks + listener[0] * FPS
            if not listener[3]:
                _timed_event_listeners.remove(listener)
    
    for event in _queue:
        if not event[1]: _queue.remove(event)
    
    for timeout in _timeouts:
        if timeout[0] <= 0:
            timeout[1]()
            _timeouts.remove(timeout)

        else: timeout[0] -= 1


append_loop(update_all)