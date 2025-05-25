from collections import defaultdict, Counter

def sum_reducer(key, values):
    """Reduce stage: Aggregates quantity sum by key."""
    # key is (date, context), values is a list of quantities
    if not values:
        return 0
    # Ensure values is a list of integers or floats 
    return sum(values)
