import unittest
import json
from datetime import datetime
from json_tools.json_extension import TaggedJSONEncoder, tagged_decoder_hook

class TestJSONExtension(unittest.TestCase):

    def test_encode_decode_set(self):
        data = {"myset": {1, 2, 3}}
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        self.assertEqual(decoded["myset"], {1, 2, 3})
        self.assertIsInstance(decoded["myset"], set)

    def test_encode_decode_datetime(self):
        now = datetime.now()
        data = {"mydate": now}
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        self.assertEqual(decoded["mydate"], now)
        self.assertIsInstance(decoded["mydate"], datetime)

    def test_encode_decode_date(self):
        from datetime import date
        today = date.today()
        data = {"today": today}
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        self.assertEqual(decoded["today"], today)
        self.assertIsInstance(decoded["today"], date)

    def test_encode_decode_int_keys(self):
        data = {1: "one", 2: "two", "three": 3}
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        self.assertEqual(decoded[1], "one")
        self.assertEqual(decoded[2], "two")
        self.assertEqual(decoded["three"], 3)
        self.assertIn(1, decoded)
        self.assertNotIn("1", decoded)

    def test_nested_structures(self):
        data = {
            "list": [1, {2, 3}],
            "dict": {
                4: datetime(2023, 1, 1),
                "set": {5}
            }
        }
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        
        self.assertEqual(decoded["list"][1], {2, 3})
        self.assertEqual(decoded["dict"][4], datetime(2023, 1, 1))
        self.assertEqual(decoded["dict"]["set"], {5})

    def test_encode_decode_tuple(self):
        data = {"mytuple": (1, 2, 3)}
        json_str = json.dumps(data, cls=TaggedJSONEncoder)
        decoded = json.loads(json_str, object_hook=tagged_decoder_hook)
        self.assertEqual(decoded["mytuple"], (1, 2, 3))
        self.assertIsInstance(decoded["mytuple"], tuple)

if __name__ == '__main__':
    unittest.main()
