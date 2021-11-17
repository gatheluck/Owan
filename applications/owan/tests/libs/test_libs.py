import pytest

import owan.libs.storage


class TestKey:
    @pytest.mark.parametrize("filename", ["file_a", "ファイル_甲"])
    def test_generate(self, filename):
        key = owan.libs.storage.Key.generate(filename)
        assert key.filename == filename

    @pytest.mark.parametrize("filename", ["file_a", "ファイル_甲"])
    def test_serialize_deserialize(self, filename):
        key = owan.libs.storage.Key.generate(filename)
        serialized = key.serialize()
        assert key == owan.libs.storage.Key.deserialize(serialized)
