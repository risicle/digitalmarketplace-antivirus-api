from flask import current_app, abort, request


def requires_authentication(module='main'):
    if current_app.config['AUTH_REQUIRED']:
        incoming_token = get_token_from_headers(request.headers)

        if not incoming_token:
            abort(401, "Unauthorized; bearer token must be provided")
        if not token_is_valid(incoming_token, module=module):
            abort(403, "Forbidden; invalid bearer token provided {}".format(incoming_token))


def token_is_valid(incoming_token, module):
    return incoming_token in get_allowed_tokens_from_config(current_app.config, module=module)


def get_allowed_tokens_from_config(config, module='main'):
    """Return a list of allowed auth tokens from the application config"""
    env_variable_name = 'DM_AV_AUTH_TOKENS'

    if module == 'callbacks':
        env_variable_name = 'DM_API_CALLBACK_AUTH_TOKENS'

    return [token for token in config.get(env_variable_name, '').split(':') if token]


def get_token_from_headers(headers):
    auth_header = headers.get('Authorization', '')
    if auth_header[:7] != 'Bearer ':
        return None
    return auth_header[7:]
