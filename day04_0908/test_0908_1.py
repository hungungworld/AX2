import os
import pandas as pd

def test_load_and_filter_data():
    # Since the module starts with a digit, we import it dynamically
    import importlib
    app = importlib.import_module("0908_1")
    
    csv_path = r"C:\Users\user\AX2\common\raw_trade_data.csv"
    assert os.path.exists(csv_path), f"Raw data file {csv_path} does not exist"
    
    top_10 = app.load_and_filter_data(csv_path)
    
    # Verify shape
    assert isinstance(top_10, pd.DataFrame), "Result must be a pandas DataFrame"
    assert len(top_10) == 10, f"Result must have exactly 10 rows, got {len(top_10)}"
    
    # Verify HS Code filter: starts with 85
    for hs in top_10['hs_code']:
        assert str(hs).startswith('85'), f"HS code {hs} does not start with 85"
        
    # Verify Country filter: '미국' or '베트남'
    for country in top_10['국가명']:
        assert country in ['미국', '베트남'], f"Country {country} is not '미국' or '베트남'"
        
    # Verify Export Amount: > 0
    for amt in top_10['수출금액']:
        assert amt > 0, f"Export amount {amt} must be greater than 0"
        
    # Verify Sort: sorted in descending order by 수출금액
    amounts = list(top_10['수출금액'])
    assert amounts == sorted(amounts, reverse=True), "Results are not sorted in descending order by 수출금액"
    
    print("✅ All unit tests passed successfully!")

if __name__ == "__main__":
    test_load_and_filter_data()
