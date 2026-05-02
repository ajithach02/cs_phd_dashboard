# test_data.py
# Basic tests to verify the dataset loads and filters correctly
# Running this file should print green checkmarks for all 4 tests

import pandas as pd

def test_load_data():
    # make sure the CSV actually loads and has all the columns we need
    df = pd.read_csv("data/phd_programs.csv")
    assert not df.empty, "Dataset should not be empty"
    expected_cols = ["university", "rank", "stipend_monthly", "acceptance_rate", "research_area"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
    print("✅ test_load_data passed")

def test_filter_by_research_area():
    # check that filtering by research area actually works and doesn't return wrong results
    df = pd.read_csv("data/phd_programs.csv")
    filtered = df[df["research_area"] == "Machine Learning"]
    assert len(filtered) > 0, "Should have Machine Learning programs"
    assert all(filtered["research_area"] == "Machine Learning")
    print("✅ test_filter_by_research_area passed")

def test_stipend_range():
    # all stipends should be between $2000 and $5000 — anything outside that is probably bad data
    df = pd.read_csv("data/phd_programs.csv")
    assert df["stipend_monthly"].min() >= 2000, "Stipend too low"
    assert df["stipend_monthly"].max() <= 5000, "Stipend too high"
    print("✅ test_stipend_range passed")

def test_no_missing_values():
    # missing university names or ranks would break the charts so checking for those here
    df = pd.read_csv("data/phd_programs.csv")
    assert df["university"].isnull().sum() == 0, "Missing university names"
    assert df["rank"].isnull().sum() == 0, "Missing ranks"
    print("✅ test_no_missing_values passed")

# run all tests when this file is executed directly
if __name__ == "__main__":
    test_load_data()
    test_filter_by_research_area()
    test_stipend_range()
    test_no_missing_values()
    print("\n✅ All tests passed!")