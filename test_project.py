from project import file_exists, write_to_csv, remove


fields = ["posted_date", "posted_time", "description", "time", "date"]

file = "test.csv"

messages = {
    "posted_date": "today",
    "posted_time": "now",
    "description": "running test",
    "time": "test now",
    "date": "test date",
}

text_raw = ["this", "\n", "is", "", "a", "#EAR", "test"]


def test_file_exists():
    assert file_exists(fields, file) == None


def test_write_to_csv():
    assert write_to_csv(fields, file, messages) == True


def test_remove():
    assert remove(text_raw) == ["this", "is", "a", "test"]
