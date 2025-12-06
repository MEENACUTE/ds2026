from functools import reduce
import re
from collections import defaultdict

def mapper(chunk):
    """Mapper: Find local max length and paths with that length in the chunk."""
    if not chunk:
        return []
    max_len = max(len(path.strip()) for path in chunk)  # Strip newlines if from file
    longest = [path.strip() for path in chunk if len(path.strip()) == max_len]
    return [(1, (max_len, longest))]  # Dummy key 1 for single reducer group

def shuffle_sort(map_outputs):
    """Shuffle and Sort: Group by key (all to one group)."""
    grouped = defaultdict(list)
    for output in map_outputs:
        for key, value in output:
            grouped[key].append(value)
    return list(grouped.items())  # List of (key, list_of_values)

def reducer(key_values):
    """Reducer: Merge local maxes, find global max, and collect matching paths."""
    key, locals = key_values
    if not locals:
        return None
    all_max_lens = [loc[0] for loc in locals]
    global_max = max(all_max_lens)
    longest_paths = []
    for max_len, paths in locals:
        if max_len == global_max:
            longest_paths.extend(paths)
    return (global_max, longest_paths)

def map_reduce(path_chunks):
    # Map phase
    map_outputs = [mapper(chunk) for chunk in path_chunks]  # Use list comprehension for simulation
    
    # Shuffle and sort
    shuffled = shuffle_sort(map_outputs)
    
    # Reduce phase
    reduced = [reducer(item) for item in shuffled]
    
    return reduced[0] if reduced else (0, [])

# Example usage (simulating inputs from multiple "laptop" files)
sample_paths_laptop1 = ["/usr/bin/python", "/etc/hosts", "/var/log/syslog"]
sample_paths_laptop2 = ["/home/user/documents/longpath.txt", "/tmp/short"]
sample_paths_laptop3 = ["/very/long/path/to/file/in/deep/directory/structure.txt", "/another/long/one.txt"]
chunks = [sample_paths_laptop1, sample_paths_laptop2, sample_paths_laptop3]  # Each chunk simulates a file/laptop
result = map_reduce(chunks)
print(f"Longest length: {result[0]}")
print("Longest paths:", result[1])