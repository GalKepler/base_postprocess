import logging


def execute(step_name: str, runner, logger: logging.Logger, inputs: dict):
    """
    Execute a step.

    Parameters
    ----------
    step_name : str
        The name of the step.
    runner : NiPype runner
        A NiPype runner.
    logger : logging.Logger
        A logger.
    inputs : dict
        The inputs to the step.
    """
    if logger:
        logger.info(f"Running {step_name} with inputs: {inputs}")
        logger.info("Executing: ")
    runner.run()
    if logger:
        logger.info(f"Finished running {step_name}")
