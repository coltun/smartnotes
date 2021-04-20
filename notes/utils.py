
"""Function explained:
Extracting the hashtags from a string text while:
1. ignoring hashtags from string urls. 
2. removes hashtags duplicates from string if any.
"""
def extract_hash_tags(s):
	return set(part for part in s.split() if part.startswith('#'))