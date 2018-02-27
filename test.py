import io
import json
import unittest
import urllib2
import datetime
from dropbox import dropbox, Stream

orig_urlopen = urllib2.urlopen

BASE_URL = "https://api.dropboxapi.com/2/team"

OPTIONS = {
    "logger": lambda *msgs: None,  # no-op logger
    "past_days": 3
}


class TestDropboxTeam(unittest.TestCase):

    def tearDown(self):
        urllib2.urlopen = orig_urlopen

    def test_get_endpoints(self):
        def test_for_code(code, msg):
            httpError = urllib2.HTTPError('msg', code, *[None] * 3)

            def urlopen(req):
                raise httpError

            urllib2.urlopen = urlopen

            try:
                dropbox.get_endpoints('token')
                self.fail("expecting an error")
            except Exception as e:
                self.assertEqual(e.message, msg)

        test_for_code(400, dropbox.AUTH_ERROR_MSG)
        test_for_code(401, dropbox.AUTH_ERROR_MSG)
        test_for_code(500, dropbox.VALIDATE_ERROR_MSG)

        # now test without error
        def urlopen(req):
            return io.BytesIO(json.dumps(""))
        urllib2.urlopen = urlopen
        endpoints = dropbox.get_endpoints('token')
        self.assertEqual(endpoints, dropbox.ENDPOINTS)

    def test_dest(self):
        source = {
            "token": "abc",
            "endpoints": ["devices/list_members_devices"]
        }

        Stream(source, OPTIONS)
        self.assertEqual(source["destination"], "dropbox_teams")

    def test_list_members_devices(self):
        res = [
            {
                "devices": [
                    {"hello": "world"},
                    {"foo": "bar"}
                ],
                "has_more": True,
                "cursor": "111"
            },
            {
                "devices": [
                    {"alice": "bob"}
                ],
                "has_more": False
            }
        ]

        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps(res.pop(0)))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["devices/list_members_devices"]
        }, OPTIONS)

        data = d.read()

        self.assertEqual(data, [
            {"hello": "world"},
            {"foo": "bar"}
        ])

        self.assertEqual(len(reqs), 1)

        url = "{}/devices/list_members_devices".format(BASE_URL)
        self.assertEqual(reqs[0].get_full_url(), url)
        self.assertEqual(reqs[0].get_data(), '{}')

        # read more
        data = d.read()
        self.assertEqual(data, [
            {"alice": "bob"}
        ])

        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[1].get_data(), '{"cursor": "111"}')

        # should be done
        data = d.read()
        self.assertEqual(data, None)

    def test_groups_list(self):
        res = [
            {
                "groups": [
                    {"hello": "world"},
                    {"foo": "bar"}
                ],
                "has_more": True,
                "cursor": "111"
            },
            {
                "groups": [
                    {"alice": "bob"}
                ],
                "has_more": False
            }
        ]

        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps(res.pop(0)))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["groups/list"]
        }, OPTIONS)

        data = d.read()

        self.assertEqual(data, [
            {"hello": "world"},
            {"foo": "bar"}
        ])

        self.assertEqual(len(reqs), 1)

        expected = "{}/groups/list".format(BASE_URL)
        self.assertEqual(reqs[0].get_full_url(), expected)
        self.assertEqual(reqs[0].get_data(), "{}")

        # read more
        data = d.read()

        self.assertEqual(data, [
            {"alice": "bob"}
        ])

        self.assertEqual(len(reqs), 2)
        expected = "{}/groups/list/continue".format(BASE_URL)
        self.assertEqual(reqs[1].get_full_url(), expected)
        self.assertEqual(reqs[1].get_data(), '{"cursor": "111"}')

        # # should be done
        data = d.read()
        self.assertEqual(data, None)

    def test_list_apps(self):
        res = [
            {
                "apps": [
                    {"hello": "world"},
                    {"foo": "bar"}
                ],
                "has_more": True,
                "cursor": "111"
            },
            {
                "apps": [
                    {"alice": "bob"}
                ],
                "has_more": False
            }
        ]

        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps(res.pop(0)))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["linked_apps/list_members_linked_apps"]
        }, OPTIONS)

        data = d.read()

        self.assertEqual(data, [
            {"hello": "world"},
            {"foo": "bar"}
        ])

        self.assertEqual(len(reqs), 1)

        expected = "{}/linked_apps/list_members_linked_apps".format(BASE_URL)
        self.assertEqual(reqs[0].get_full_url(), expected)
        self.assertEqual(reqs[0].get_data(), '{}')

        # read more
        data = d.read()

        self.assertEqual(data, [
            {"alice": "bob"}
        ])

        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[1].get_full_url(), expected)
        self.assertEqual(reqs[1].get_data(), '{"cursor": "111"}')

        # # should be done
        data = d.read()
        self.assertEqual(data, None)

    def test_members_list(self):
        res = [
            {
                "members": [
                    {"hello": "world"},
                    {"foo": "bar"}
                ],
                "has_more": True,
                "cursor": "111"
            },
            {
                "members": [
                    {"alice": "bob"}
                ],
                "has_more": False
            }
        ]

        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps(res.pop(0)))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["members/list"]
        }, OPTIONS)

        data = d.read()

        self.assertEqual(data, [
            {"hello": "world"},
            {"foo": "bar"}
        ])

        self.assertEqual(len(reqs), 1)

        expected = "{}/members/list".format(BASE_URL)
        self.assertEqual(reqs[0].get_full_url(), expected)
        self.assertEqual(reqs[0].get_data(), '{}')

        # read more
        data = d.read()

        self.assertEqual(data, [
            {"alice": "bob"}
        ])

        self.assertEqual(len(reqs), 2)
        expected += "/continue"
        self.assertEqual(reqs[1].get_full_url(), expected)
        self.assertEqual(reqs[1].get_data(), '{"cursor": "111"}')

        # # should be done
        data = d.read()
        self.assertEqual(data, None)

    def test_get_events(self):
        ev1 = {
            "event_type": "member_join",
            "member_id": "dbmid:ijkl9012",
            "info_dict": {
                "initial_devices": "[]",
                "initial_apps": "[]"
            },
            "ip_address": "192.0.2.0",
            "user_id": 12345678,
            "name": "Jenny",
            "country": "US",
            "event_type_description": "Joined the team",
            "event_category": "members",
            "time": "2014-10-01T17:23:05+00:00",
            "email": "jenny@example.com"
        }

        ev2 = {
            "event_type": "login_success",
            "member_id": "dbmid:efgh5678",
            "info_dict": None,
            "ip_address": "192.0.2.0",
            "user_id": 87654321,
            "name": "John",
            "country": "US",
            "event_type_description": "Signed in",
            "event_category": "logins",
            "time": "2014-10-03T01:16:32+00:00",
            "email": "john@example.com"
        }

        ev3 = {
            "event_type": "device_link",
            "member_id": "dbmid:efgh5678",
            "info_dict": None,
            "ip_address": "192.0.2.0",
            "user_id": 87654321,
            "name": "John",
            "country": "US",
            "event_type_description": "Signed in",
            "event_category": "logins",
            "time": "2014-10-03T01:16:32+00:00",
            "email": "john@example.com"
        }
        res = [
            {
                "events": [ev1, ev2],
                "has_more": True,
                "cursor": "111"
            },
            {
                "events": [ev3],
                "has_more": False
            }
        ]

        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps(res.pop(0)))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["log/get_events"]
        }, OPTIONS)

        data = d.read()

        self.assertEqual(data, [ev1, ev2])

        self.assertEqual(len(reqs), 1)

        expected = "https://api.dropboxapi.com/1/team/log/get_events"
        self.assertEqual(reqs[0].get_full_url(), expected)
        self.assertEqual(reqs[0].get_data(), '{}')

        # read more
        data = d.read()

        self.assertEqual(data, [ev3])

        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[1].get_full_url(), expected)
        self.assertEqual(reqs[1].get_data(), '{"cursor": "111"}')

        # # should be done
        data = d.read()
        self.assertEqual(data, None)

    def test_get_activity(self):
        reqs = []

        def urlopen(req):
            reqs.append(req)
            return io.BytesIO(json.dumps({
                "adds": [1, 2, 3],
                "edits": [4, 5, 6]
            }))

        urllib2.urlopen = urlopen
        d = Stream({
            "token": "abc",
            "endpoints": ["reports/get_activity"]
        }, OPTIONS)

        today = datetime.date.today()
        for i in range(OPTIONS["past_days"]):
            data = d.read()

            start = today - datetime.timedelta(OPTIONS["past_days"] - i)
            end = start + datetime.timedelta(1)

            self.assertEqual(reqs[i].get_data(), json.dumps({
                "start_date": start.isoformat(),
                "end_date": end.isoformat()
            }))
            self.assertEqual(data, [{"adds": [1, 2, 3], "edits": [4, 5, 6]}])

        expected = "{}/reports/get_activity".format(BASE_URL)
        self.assertEqual(reqs[0].get_full_url(), expected)

        # should be done
        data = d.read()
        self.assertEqual(data, None)


# fire it up.
if __name__ == "__main__":
    unittest.main()
