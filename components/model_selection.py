import os

def get_target_port(model_name):
    architect_model = os.environ.get("ARCHITECT_MODEL", "")
    coder_model = os.environ.get("CODER_MODEL", "")

    if model_name.startswith(architect_model):
        return os.environ.get("ARCHITECT_ENDPOINT", None)
    elif model_name.startswith(coder_model):
        return os.environ.get("CODER_ENDPOINT", None)
    else:
        return None
