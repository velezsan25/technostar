import re
import sys
import requests

URL = 'http://127.0.0.1:8000/registro/'

s = requests.Session()
print('GET', URL)
r = s.get(URL)
print('GET status:', r.status_code)

m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
if not m:
    # Try alternative pattern (sometimes csrf is in cookie)
    cookie_csrf = s.cookies.get('csrftoken')
    if cookie_csrf:
        csrf = cookie_csrf
        print('Found CSRF in cookie')
    else:
        print('No CSRF token found in page or cookie')
        sys.exit(1)
else:
    csrf = m.group(1)
    print('Found CSRF token in form')

payload = {
    'username': 'test_ui_user',
    'email': 'test_ui_user@example.com',
    'first_name': 'TestUI',
    'last_name': 'User',
    'password1': 'Aa123456!',
    'password2': 'Aa123456!'
}

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrf,
}

print('POST', URL, 'payload keys', list(payload.keys()))
resp = s.post(URL, data=payload, headers=headers)
print('POST status:', resp.status_code)
print('Response text:')
print(resp.text)

# Check if user exists
print('\nChecking DB via admin endpoint is not available from here; please run Django shell if needed')
