import pandas as pd

# Sample data
df = pd.DataFrame({
    'code': ['A', 'A', 'A', 'B', 'B', 'B', 'A'],
    'name': ['apple', None, None, 'banana', None, 'banana', None]
})

print("Before:")
print(df)

# Your known mappings (like a lookup table)
code_to_name = {
    'A': 'apple',
    'B': 'banana'
}

# Fill name where code matches and name is null
mask = df['name'].isnull() & df['code'].isin(code_to_name.keys())
df.loc[mask, 'name'] = df.loc[mask, 'code'].map(code_to_name)

print("\nAfter:")
print(df)
