from __future__ import absolute_import
import json
import panoply
import sys
import urllib2
import datetime
import copy
from urllib import urlencode

ONE_DAY = datetime.timedelta(1)
PAST_DAYS = 30
API_VERSION = 2

AUTH_ERROR_MSG = ('Authentication failed. Please check'
                  ' your credentials and try again')
VALIDATE_ERROR_MSG = ('An unexpected error occured while validating'
                      ' your credentials, please contact support')

ENDPOINTS = [
    {"uri": "devices/list_members_devices", "get": "devices"},
    {"uri": "groups/list", "continue": True, "get": "groups"},
    {"uri": "linked_apps/list_members_linked_apps", "get": "apps"},
    {"uri": "members/list", "continue": True, "get": "members"},
    {"uri": "log/get_events", "get": "events", "v": 1},
    {"uri": "reports/get_activity"},
    {"uri": "reports/get_devices"},
    {"uri": "reports/get_membership"},
    {"uri": "reports/get_storage"},
]


class DropboxTeam(panoply.DataSource):

    def __init__(self, source, options):
        super(DropboxTeam, self).__init__(source, options)

        if source.get("destination") is None:
            source["destination"] = "dropbox_teams"

        past_days = datetime.timedelta(options.get("past_days", PAST_DAYS))
        endpoints = source.get("endpoints", [])
        self._endpoints = map(lambda uri: Endpoint({
            "start_date": datetime.date.today() - past_days,
            "cursor": None,
            "v": API_VERSION,
            "get": None,
        }).extend([e for e in ENDPOINTS if e["uri"] == uri][0]), endpoints)

    def read(self):
        if len(self._endpoints) == 0:
            return None  # we're done here.

        # get & read from the next endpoint
        endpoint = self._endpoints[0]
        read_fn = {
            True: self._read_reports,
            False: self._read_endpoint
        }[endpoint["uri"].startswith("reports/")]

        # endpoint is done? remove it and continue to the next one.
        res, has_more = read_fn(endpoint)
        if not has_more:
            self._endpoints.pop(0)

        # some endpoints need to access a specific value within the response
        # object
        if endpoint["get"] is not None:
            res = res[endpoint["get"]]

        return res

    def _read_endpoint(self, endpoint):
        uri = endpoint["uri"]

        # build the uri and cursor data to paginate over the results
        data = {}
        if endpoint["cursor"] is not None:
            data["cursor"] = endpoint["cursor"]

            # some endpoints use a separate URL for the following requests
            # suffixed with /continue
            if endpoint.get("continue", False):
                uri += "/continue"

        # issue the http request
        res = self._request(uri, data, apiversion=endpoint["v"])

        # update the cursor to determine if we can keep going.
        endpoint["cursor"] = res.get("cursor")

        return res, res.get("has_more", False)

    def _read_reports(self, endpoint):
        start = endpoint["start_date"]
        end = start + ONE_DAY
        res = self._request(endpoint["uri"], {
            "start_date": start.isoformat(),
            "end_date": end.isoformat()
        })

        # increment the date for the next iteration
        endpoint["start_date"] = end

        return [res], endpoint["start_date"] < datetime.date.today()

    def _request(self, uri, data, apiversion="2"):
        self.log("POST", uri)
        return request(self.source.get("token"), uri, data, apiversion)


def request(token, uri, data, apiversion="2"):
    data = json.dumps(data)
    url = "https://api.dropboxapi.com/%s/team/%s" % (apiversion, uri)
    req = urllib2.Request(url, data)
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("Content-Type", "application/json")
    res = urllib2.urlopen(req)
    body = res.read()
    return json.loads(body)


def get_endpoints(token):

    try:
        # sample request to validate the token
        request(token, "groups/list", {"limit": 1})
    except urllib2.HTTPError as e:
        print(e.code)
        if(e.code in [401, 400]):
            raise Exception(AUTH_ERROR_MSG)
        raise e
    except Exception as e:
        raise Exception(VALIDATE_ERROR_MSG)

    return ENDPOINTS


class Endpoint(dict):
    def extend(self, *args):
        self.update(*args)
        return self
