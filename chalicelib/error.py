import logging

import chalicelib.response as response
from chalicelib.form import FormValidationError
from chalicelib.service import ResourceNotFoundError


def error_handler(decorated):
    """
    @app.route('/)
    @error_handler
    def route():
        pass
    :param decorated: The function implementation that will be extended with error handling
    :return: The decorated function wrapped with error handling capabilities
    """

    def wrapped_handler(*args, **kwargs):
        try:
            return decorated(*args, **kwargs)
        except ResourceNotFoundError as ex:
            return response.not_found(ex.identifier)
        except FormValidationError as ex:
            return response.bad(error_details=ex.error_details, schema=ex.schema)
        except Exception as ex:
            logging.getLogger('contact-message-service').error("Caught exception for %s", ex, exc_info=True)
            return response.internal_error()

    return wrapped_handler
