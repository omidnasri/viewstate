import pytest

from viewstate import *


class TestViewState(object):

    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    def test_is_valid(self):
        with open('tests/samples/ngcs.sample', 'r') as f:
            vs = ViewState(f.read())
            assert vs.is_valid() is True

    def test_invalid_base64(self):
        with pytest.raises(ViewStateException):
            vs = ViewState('hello')

    def test_invalid_decode(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b'\x01\x02')
            vs.decode()

    def test_parse_const_value(self):
        vs = ViewState(raw=b'\xff\x01\x67')
        assert vs.decode() is True

    def test_parse_string_value(self):
        s = 'abcdefghij'
        vs = ViewState(raw=b'\xff\x01\x05\x0a' + s.encode())
        assert vs.decode() == s

    def test_parse_simple_dict(self):
        vs = ViewState(raw=b'\xff\x01\x18\x02\x05\x01a\x05\x01b\x05\x01c\x05\x01d')
        assert vs.decode() == {'a': 'b', 'c': 'd'}

    def test_parse_simple_list(self):
        vs = ViewState(raw=b'\xff\x01\x16\x05\x05\x01a\x05\x01b\x05\x01c\x05\x01d\x05\x01e')
        assert vs.decode() == ['a', 'b', 'c', 'd', 'e']

    def test_parse_simple_pair(self):
        vs = ViewState(raw=b'\xff\x01\x0f\x67\x68')
        assert vs.decode() == (True, False)

    def test_parse_complex_pair(self):
        vs = ViewState()
        vs.raw = b'\xff\x01\x0f\x67\x0f\x68\x66'
        assert vs.decode() == (True, (False, 0))
        vs.raw = b'\xff\x01\x0f\x0f\x67\x68\x66'
        assert vs.decode() == ((True, False), 0)
        vs.raw = b'\xff\x01\x0f\x0f\x67\x05\x061q2w3e\x66'
        assert vs.decode() == ((True, '1q2w3e'), 0)

    def test_parse_unknown(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b'\xff\x01\x99\x99\x99')
            assert vs.decode()
