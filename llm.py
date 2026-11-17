import json
import os
import urllib.error
import urllib.request

def complete(messages, tools=None):
    """Explicit live call; never silently substitutes an offline response."""
    key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    if not key or not model:
        raise RuntimeError('Set OPENAI_API_KEY and OPENAI_MODEL for live mode')
    payload = {'model': model, 'messages': messages}
    if tools:
        payload['tools'] = tools
    request = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'Provider request failed: HTTP {error.code}') from None
    return result['choices'][0]['message'], result.get('usage', {})
