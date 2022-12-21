from urllib.parse import quote

from test_server import Response

from tests.util import BaseGrabTestCase, build_grab


class TestPostFeature(BaseGrabTestCase):
    def setUp(self):
        self.server.reset()

    def test_post(self):
        self.server.add_response(Response(), count=9)
        grab = build_grab(url=self.server.get_url())

        # Provide POST data in dict
        grab.setup(post={"foo": "bar"})
        grab.request()
        self.assertEqual(self.server.request.data, b"foo=bar")

        # Provide POST data in tuple
        grab.setup(post=(("foo", "TUPLE"),))
        grab.request()
        self.assertEqual(self.server.request.data, b"foo=TUPLE")

        # Provide POST data in list
        grab.setup(post=[("foo", "LIST")])
        grab.request()
        self.assertEqual(self.server.request.data, b"foo=LIST")

        # Order of elements should not be changed (1)
        grab.setup(post=[("foo", "LIST"), ("bar", "BAR")])
        grab.request()
        self.assertEqual(self.server.request.data, b"foo=LIST&bar=BAR")

        # Order of elements should not be changed (2)
        grab.setup(post=[("bar", "BAR"), ("foo", "LIST")])
        grab.request()
        self.assertEqual(self.server.request.data, b"bar=BAR&foo=LIST")

        # Provide POST data in byte-string
        grab.setup(post="Hello world!")
        grab.request()
        self.assertEqual(self.server.request.data, b"Hello world!")

        # Provide POST data in unicode-string
        grab.setup(post="Hello world!")
        grab.request()
        self.assertEqual(self.server.request.data, b"Hello world!")

        # Provide POST data in non-ascii unicode-string
        grab.setup(post="Привет, мир!")
        grab.request()
        self.assertEqual(self.server.request.data, "Привет, мир!".encode("utf-8"))

        # Two values with one key
        grab.setup(post=(("foo", "bar"), ("foo", "baz")))
        grab.request()
        self.assertEqual(self.server.request.data, b"foo=bar&foo=baz")

    def test_multipart_post(self):
        self.server.add_response(Response(), count=3)
        grab = build_grab(url=self.server.get_url())
        # Dict
        grab.setup(multipart_post={"foo": "bar"})
        grab.request()
        self.assertTrue(b'name="foo"' in self.server.request.data)

        # tuple with one pair
        grab.setup(multipart_post=(("foo", "bar"),))
        grab.request()
        self.assertTrue(b'name="foo"' in self.server.request.data)

        # tuple with two pairs
        grab.setup(multipart_post=(("foo", "bar"), ("foo", "baz")))
        grab.request()
        self.assertTrue(b'name="foo"' in self.server.request.data)

    def test_unicode_post(self):
        self.server.add_response(Response(), count=3)
        # By default, unicode post should be converted into utf-8
        grab = build_grab()
        data = "фыва"
        grab.setup(post=data, url=self.server.get_url())
        grab.request()
        self.assertEqual(self.server.request.data, data.encode("utf-8"))

        # Now try cp1251 with encoding option
        grab = build_grab()
        data = "фыва"
        grab.setup(post=data, url=self.server.get_url(), encoding="cp1251")
        grab.request()
        self.assertEqual(self.server.request.data, data.encode("cp1251"))

        # Now try dict with unicode value & encoding option
        grab = build_grab()
        data = "фыва"
        grab.setup(post={"foo": data}, url=self.server.get_url(), encoding="cp1251")
        grab.request()
        test = ("foo=%s" % quote(data.encode("cp1251"))).encode("ascii")
        self.assertEqual(self.server.request.data, test)

    def test_put(self):
        self.server.add_response(Response())
        grab = build_grab()
        grab.setup(post=b"abc", url=self.server.get_url(), method="put")
        grab.request()
        self.assertEqual(self.server.request.method, "PUT")
        self.assertEqual(self.server.request.headers.get("content-length"), "3")

    def test_patch(self):
        self.server.add_response(Response())
        grab = build_grab()
        grab.setup(post=b"abc", url=self.server.get_url(), method="patch")
        grab.request()
        self.assertEqual(self.server.request.method, "PATCH")
        self.assertEqual(self.server.request.headers.get("content-length"), "3")

    def test_empty_post(self):
        self.server.add_response(Response(), count=2)
        grab = build_grab()
        grab.setup(method="post", post="")
        grab.request(self.server.get_url())
        self.assertEqual(self.server.request.method, "POST")
        self.assertEqual(self.server.request.data, b"")
        self.assertEqual(self.server.request.headers.get("content-length"), "0")

        grab.request(self.server.get_url(), post="DATA")
        self.assertEqual(self.server.request.headers.get("content-length"), "4")

    def test_post_multivalue_key(self):
        self.server.add_response(Response())
        grab = build_grab()
        grab.setup(post=[("foo", [1, 2])])
        grab.request(self.server.get_url())
        self.assertEqual(self.server.request.data, b"foo=1&foo=2")
