from loguru import logger
import functools


def __msg_formatter(error_msg, arg_tuple, arg_name):
    if (len(arg_tuple) > 0):
        error_msg += "\n" + arg_name + ":{}".format(arg_tuple)
    return error_msg


def log_wrapper(log_start: bool = True, log_end: bool = True, log_exception: bool = True, throw_exception: bool = True):
    '''
    Python decorator to log exceptions.

    **You still need to do `loguru.logger.add(file_name)` to create proper sinks o/w it is sent to command line by default.**

    Parameter
    ---------
    log_start : bool, default: True
        Whether to log the start of the function. Uses logger.debug()
    log_end : bool, default: True
        Whether to log the end of the function. Uses logger.debug()
    log_exception : bool, default: True
        Whether to log the exception of the function. Uses logger.error()
    throw_exception : bool, default: True
        Whether to consume the exception or throw the exception to caller.

    Example
    -------

    >>> @log_wrapper()
        def divide(num1, num2)
            return num1 / num2

    >>> divide(1/2)
    2021-02-23 15:56:36.829 | DEBUG    | __main__:wrapper:25 - Start executing function: divide
    2021-02-23 15:56:36.830 | DEBUG    | __main__:wrapper:37 - Finished executing function: divide

    >>> divide()
    2021-02-23 15:56:36.831 | DEBUG    | __main__:wrapper:25 - Start executing function: divide
    2021-02-23 15:56:36.832 | ERROR    | __main__:wrapper:32 -
    Function: divide
    Message: divide() missing 2 required positional arguments: 'num1' and 'num2'
    2021-02-23 15:56:36.833 | DEBUG    | __main__:wrapper:37 - Finished executing function: divide
    '''

    def log_wrapper_2(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f"Start executing function: {func.__name__}")
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = "\n" + f"Function: {func.__name__}"
                error_msg = __msg_formatter(error_msg, args, "Args")
                error_msg = __msg_formatter(error_msg, kwargs, "Kwargs")
                error_msg += "\n" + f"Message: {e}"
                logger.error(error_msg)

                if (throw_exception):
                    return e
            finally:
                logger.debug(f"Finished executing function: {func.__name__}")

        return wrapper
    return log_wrapper_2
