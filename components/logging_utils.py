import json
import os

LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

def log_to_file(filename, endpoint, content=None, stream=False, is_final=False):
    filepath = os.path.join(LOGS_DIR, filename)
    with open(filepath, 'a') as f:
        if content is not None:
            json.dump(content, f)
        if not stream or is_final:
            f.write('\n\n')
