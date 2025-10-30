import urllib.request, urllib.parse, http.cookiejar, re, sys, json
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# GET the registration page to get CSRF token
url = 'http://127.0.0.1:8000/registro/'
resp = opener.open(url)
html = resp.read().decode('utf-8', errors='replace')
m = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\'](.+?)["\']', html)
if not m:
    m = re.search(r'value=["\'](.+?)["\']\s+name=["\']csrfmiddlewaretoken["\']', html)
if not m:
    print('CSRF token not found in registration page')
    sys.exit(1)
csrftoken = m.group(1)
print('CSRF token:', csrftoken)
# Prepare registration data
username = 'testuser_ai'
email = 'testuser_ai@example.com'
first_name = 'Test'
last_name = 'User'
password = 'TestPass123!'
post_data = {
    'username': username,
    'email': email,
    'first_name': first_name,
    'last_name': last_name,
    'password1': password,
    'password2': password,
    'csrfmiddlewaretoken': csrftoken
}
encoded = urllib.parse.urlencode(post_data).encode()
req = urllib.request.Request(url, data=encoded, headers={
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/x-www-form-urlencoded'
})
try:
    r = opener.open(req)
    body = r.read().decode('utf-8')
    print('Status', r.getcode())
    print('Response body:', body)
    try:
        print('JSON:', json.loads(body))
    except Exception as e:
        print('No JSON:', e)
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    print('HTTPError', e.code)
    print(body)
    try:
        print('JSON:', json.loads(body))
    except Exception as e:
        print('No JSON on error:', e)
