
def demand_context_mapper(row):
    """
    Map stage: Produces a list of (context, product) pairs.
    """
    # Example: key is (Date, context), value is Quantity
    # Adjust field names as per your dataset
    date = row["InvoiceDate"]
    context = (row["Country"], row["Description"])  # or build context from multiple columns
    quantity = row["Quantity"]
    return [((date, context), quantity)]
