import pandas

df = pandas.read_csv('mapping.csv', sep='\t')
print(df['ENV'][0])
print(len(df['ENV']))