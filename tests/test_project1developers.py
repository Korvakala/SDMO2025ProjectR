import pytest
import pandas as pd
from project1developers import *


# Test Data
# tmp_path = temporary directory for testing
@pytest.fixture
def tmp_csv_file(tmp_path):
    csv_file = tmp_path / "devs.csv"
    with open(csv_file, "w", newline='',encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(["name", "email"])
        writer.writerow(["Biggus Dickus", "biggus.dickus@monty.com"])
        writer.writerow(["Incontinentia Buttocks", "incontinentia.buttocks@monty.com"])
    return tmp_path, "devs.csv"

# -------------------
# read_devs()
# -------------------

def test_read_devs(tmp_csv_file):
    path, csv_name = tmp_csv_file
    devs = read_devs(path, csv_name)
    assert len(devs) == 2, "Header was not removed"
    assert devs[0] ==  ["Biggus Dickus", "biggus.dickus@monty.com"]
    assert devs[1] == ["Incontinentia Buttocks", "incontinentia.buttocks@monty.com"]

# -------------------
# compute_similarity()
# -------------------

def test_compute_similarity():
    data = [
        ["John Doe", "john.doe@example.com"],
        ["Jon Doe", "jon.d@example.com"],
        ["Alice Smith", "alice@example.com"]]
    sim_data = compute_similarity(data)
    # sim_data should be 3 long due to 3 pairs
    assert len(sim_data) == 3
    # Every row should have 12 columns
    for row in sim_data:
        assert len(row) == 12
        # was similarity score calculated
        assert isinstance(row[4], float) # c1
        assert isinstance(row[5], float) # c2
        assert isinstance(row[6], float) # c31
        assert isinstance(row[7], float) # c32

# -------------------
# Preprocess()
# -------------------

def test_preprocess():
    # Normal name
    dev = [" Biggus. Dickus!", "biggus.dickus@monty.com"]
    name, first, last, i_first, i_last, email, prefix = preprocess(dev)
    assert name == "biggus dickus"
    assert first == "biggus"
    assert last == "dickus"
    assert i_first == "b"
    assert i_last == "d"
    assert email == "biggus.dickus@monty.com"
    assert prefix == "biggus.dickus"

def test_preprocess_single():
    # Single part name
    dev = ["Matt", "Matt.Walker@sample.ai"]
    name, first, last, i_first, i_last, email, prefix = preprocess(dev)
    assert name == "matt"
    assert first == "matt"
    assert last == ""
    assert i_first == "m"
    assert i_last == ""
    assert email == "Matt.Walker@sample.ai"
    assert prefix == "Matt.Walker"

def test_preprocess_multipart():
    # Multi part name
    dev = ["Martin Luther King", "MartinLuther.King@ihaveadream.com"]
    name, first, last, i_first, i_last, email, prefix = preprocess(dev)
    assert name == "martin luther king"
    assert first == "martin"
    assert last == "luther king"
    assert i_first == "m"
    assert i_last == "l"
    assert email == "MartinLuther.King@ihaveadream.com"
    assert prefix == "MartinLuther.King", "email prefix wrong"

def test_preprocess_accents():
    # Accents
    dev = ["Élisè Gebârdieu", "Elise.Gebardieu@gmail.com"]
    name, first, last, i_first, i_last, email, prefix = preprocess(dev)
    assert name == "elise gebardieu"
    assert first == "elise"
    assert last == "gebardieu"
    assert i_first == "e"
    assert i_last == "g"
    assert email == "Elise.Gebardieu@gmail.com"
    assert prefix == "Elise.Gebardieu"

# -------------------
# save_similarity()
# -------------------

def test_save_similarity_data(tmp_path):
    df = pd.DataFrame(
        [["a", "b", "c", "d", 0.9, 0.8, 0.7, 0.6, False, False, False, True]],
        columns=["name_1", "email_1", "name_2", "email_2", "c1", "c2", "c3.1", "c3.2", "c4", "c5", "c6", "c7"],
    )
    save_similarity_data(df, tmp_path)
    devs_file = tmp_path / "devs_similarity.csv"
    assert devs_file.exists()
    DEVS = []
    with open(devs_file, "r", newline='',encoding="utf-8") as devs:
        reader = csv.reader(devs, delimiter=",")
        for row in reader:
            DEVS.append(row)
    DEVS = DEVS[1:]
    assert DEVS[0][0] == "a"
    assert DEVS[0][4] == "0.9"
    assert DEVS[0][-1] == "True"

# -------------------
# filter_and_save()
# -------------------

def test_filter_and_save(tmp_path):
    sim_data = [
        ["John", "a@example.com", "Jon", "b@example.com", 0.95, 0.94, 0.92, 0.90, False, False, False, False],
        ["Alice", "a@example.com", "Alice", "a@example.com", 0.5, 0.4, 0.3, 0.2, False, False, False, False],
    ]
    filter_and_save(sim_data, 0.9, tmp_path)
    output = tmp_path / "devs_similarity_t=0.9.csv"
    df = pd.read_csv(output)
    assert len(df) == 2 # Expecting two rows
    assert set(df.columns) == {
        "name_1", "email_1", "name_2", "email_2",
        "c1", "c2", "c3.1", "c3.2", "c4", "c5", "c6", "c7"
    }
 