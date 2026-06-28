from project import generatePassword, getDateFormats


def test_generatePassword():
    assert generatePassword(15, 5, 2025, "ddmmyyyy") == "15052025"
    assert generatePassword(15, 5, 2025, "yyyymmdd") == "20250515"
    assert generatePassword(15, 5, 2025, "ddmmyy") == "150525"


def test_getDateFormats():
    formats = getDateFormats()
    assert len(formats) == 5
    assert "ddmmyyyy" in formats.values()


def test_generatePassword_edge():
    assert generatePassword(1, 1, 2000, "mmddyyyy") == "01012000"
    assert generatePassword(31, 12, 1999, "ddmmyy") == "311299"
