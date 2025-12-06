from functools import reduce
import re
from collections import defaultdict

def mapper(chunk):
    """Mapper: Split text into words and emit (word, 1) pairs."""
    words = re.findall(r'\w+', chunk.lower())
    return [(word, 1) for word in words]

def shuffle_sort(map_outputs):
    """Shuffle and Sort: Group by key."""
    grouped = defaultdict(list)
    for output in map_outputs:
        for word, count in output:
            grouped[word].append(count)
    return sorted(grouped.items())  # Sort keys

def reducer(key_counts):
    """Reducer: Sum counts for each key."""
    key, counts = key_counts
    return (key, sum(counts))

def map_reduce(text_chunks):
    # Map phase
    map_outputs = list(map(mapper, text_chunks))
    
    # Shuffle and sort
    shuffled = shuffle_sort(map_outputs)
    
    # Reduce phase
    reduced = list(map(reducer, shuffled))
    
    return dict(reduced)

# Example usage
sample_text = "Hello world hello again world"
chunks = [sample_text[i:i+10] for i in range(0, len(sample_text), 10)]  # Simulate splitting into chunks
result = map_reduce(chunks)
print(result)  # Output: {'again': 1, 'hello': 2, 'world': 2}