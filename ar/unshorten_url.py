import http.client
import urllib.parse


# Returns unshortened URL if succesfull
def unshorten_url(url, count=None):
    if count is None:
        count = 0
    elif count is 3:
        return ""
    else:
        count = count + 1;
    parsed = urllib.parse.urlparse(url)
    h = http.client.HTTPConnection(parsed.netloc, timeout=20000)
    resource = parsed.path
    if parsed.query != "":
        resource += "?" + parsed.query
    h.request('HEAD', resource)
    response = h.getresponse()
    if response.status == 301 and response.getheader('Location'):
        return unshorten_url(response.getheader('Location'), count)
    else:
        return url
