class TestClass1:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")


# Path: test_class2.py


class TestClass2:
    def test_one(self):
        x = "that"
        assert "e" in x

    def test_two(self):
        x = "goodbye"
        assert x == "hello"
