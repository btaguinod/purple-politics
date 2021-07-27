from flask_restful import request, abort


def get_param(param_name, default, is_valid, to_value, error_message):
    param_string = request.args.get(param_name)
    if param_string is None:
        param_string = default
    elif not is_valid(param_string):
        abort(400, message=error_message)
    return to_value(param_string)


def get_string_param(param_name: str, default: str, valid_words: list[str]) \
        -> str:
    """Get query parameter in form of string.

    Args:
        param_name (str): Name of parameter.
        default (str): Default value of parameter.
        valid_words (list[str]): List of valid strings.
    """
    is_valid = valid_words.__contains__

    def to_value(string): return string

    error_message = f'{param_name} should be: ' + ', '.join(valid_words)
    return get_param(param_name, default, is_valid, to_value, error_message)


def get_bool_param(param_name: str, default: bool) -> bool:
    """Get query parameter in form of boolean.

    Args:
        param_name (str): Name of parameter.
        default (bool): Default value of parameter.
    """
    default = str(default).lower()
    is_valid = ['true', 'false'].__contains__

    def to_value(string): return string == "true"

    error_message = f'{param_name} should be "true" or "false"'
    return get_param(param_name, default, is_valid, to_value, error_message)


def get_int_param(param_name: str, default: int) -> int:
    """Get query parameter in form of integer.

    Args:
        param_name (str): Name of parameter.
        default (int): Default value of parameter.
    """
    default = str(default)
    is_valid = str.isdigit
    to_value = int
    error_message = f'{param_name} should be an integer'
    return get_param(param_name, default, is_valid, to_value, error_message)