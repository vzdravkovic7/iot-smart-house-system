from datetime import datetime

_state = {}

def update_state(measurement, name, value, runs_on, simulated):
    _state[name] = {
        "measurement": measurement,
        "name": name,
        "value": value,
        "runs_on": runs_on,
        "simulated": simulated,
        "timestamp": datetime.utcnow().isoformat()
    }

def get_state(name):
    return _state.get(name)

def get_all_state():
    return _state
