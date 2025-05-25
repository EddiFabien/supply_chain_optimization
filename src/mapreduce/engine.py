class MapReduceEngine:
    def __init__(self, mapper, reducer):
        self.mapper = mapper
        self.reducer = reducer

    def _map_stage(self, data_source):
        # data_source is a DataFrame
        mapped = []
        for _, row in data_source.iterrows():
            mapped.extend(self.mapper(row))
        return mapped

    def _shuffle_stage(self, mapped):
        from collections import defaultdict
        shuffled = defaultdict(list)
        for key, value in mapped:
            shuffled[key].append(value)
        return shuffled

    def _reduce_stage(self, shuffled):
        reduced = {}
        for key, values in shuffled.items():
            reduced[key] = self.reducer(key, values)
        return reduced

    def execute(self, data_source):
        mapped = self._map_stage(data_source)
        shuffled = self._shuffle_stage(mapped)
        reduced = self._reduce_stage(shuffled)
        return reduced