# src/mapreduce/run_job.py - Add these job functions

def run_demand_analysis_job(data_source):
    """
    Run complete demand analysis by context (Date, Context, Description).
    
    Args:
        data_source: CSV file path or DataFrame with demand data
        
    Returns:
        Dictionary with total quantities by context
    """
    print("=== Running Demand Analysis by Context (Date, Country, Description) ===")
    
    from engine import MapReduceEngine
    from mapper import demand_context_mapper
    from reducer import sum_reducer
    
    engine = MapReduceEngine(demand_context_mapper, sum_reducer)
    results = engine.execute(data_source)
    
    return results




if __name__ == "__main__":
    import sys
    import pandas as pd
    import os

    if len(sys.argv) < 2:
        print("Usage: python run_mapreduce.py <data_source>")
        sys.exit(1)

    data_source = sys.argv[1]
    _, ext = os.path.splitext(data_source)
    ext = ext.lower()

    if ext == ".csv":
        df = pd.read_csv(data_source)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(data_source)
    else:
        print(f"Unsupported file type: {ext}")
        sys.exit(1)

    results = run_demand_analysis_job(df)

    # Save results to dataset/data_processed/ as CSV with columns ["Date", "context", "Quantity"]
    output_dir = "dataset/data_processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "demand_processed.csv")

    # Each key in results is (date, context), value is quantity
    results_df = pd.DataFrame(
        [(date, context, quantity) for (date, context), quantity in results.items()],
        columns=["Date", "context", "Quantity"]
    )
    results_df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")


