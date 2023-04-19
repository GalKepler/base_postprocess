from base_postprocess.bids.layout.layout import QSIPREPLayout


def collect_requirements(layout: QSIPREPLayout, subject: str, requirements: dict):
    """
    Collect the requirements for a procedure.

    Parameters
    ----------
    layout : QSIPREPLayout
        A QSIPREPLayout object.
    subject : str
        The subject to collect the requirements for.
    requirements : dict
        A dictionary containing the requirements.

    Returns
    -------
    dict
        A dictionary containing the requirements.

    Raises
    ------
    ValueError
        If the scope is unknown.
    """
    result = {}
    for key, description in requirements.items():
        scope = description["scope"]
        entities = description["entities"].copy()
        entities["subject"] = subject
        if scope == "session":
            result[key] = {}
            for session in layout.get_sessions(subject=subject):
                entities["session"] = session
                value = get_file_by_entities(layout, entities)
                result[key][session] = value
        elif scope == "subject":
            value = get_file_by_entities(layout, entities)
            result[key] = value
    return result


def get_file_by_entities(layout: QSIPREPLayout, entities: dict):
    """
    Get a file from the layout by entities.

    Parameters
    ----------
    layout : QSIPREPLayout
        A QSIPREPLayout object.
    entities : dict
        A dictionary containing the entities.

    Returns
    -------
    str
        The path to the file.
    """
    result = layout.get(**entities, return_type="file")
    if len(result) > 1:
        raise ValueError(f"More than one file found for {entities}")
    return result[0]
