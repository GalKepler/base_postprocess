from collections import defaultdict


def parse_inputs_to_sessions(inputs: dict) -> dict:
    """
    Parse the inputs to a dictionary of sessions.
    """
    result = defaultdict(dict)
    for key, value in inputs.items():
        if isinstance(value, dict):
            for session, session_value in value.items():
                if session not in result:
                    result[session] = {}
                result[session][key] = session_value
        else:
            result[key] = value
    return result
