import os
import requests
import pandas as pd

# Set the GraphQL endpoint URL and query
api_key = os.environ['GRAPHQL_API_KEY']
url = 'https://gateway.thegraph.com/api/[api-key]/subgraphs/id/DTcDcUSBRJjz9NeoK5VbXCVzYbRTyuBwdPUqMi8x32pY'.replace(
  '[api-key]', api_key)
query = '''
query {
  protocolMetrics(
    first: 1000,
    orderBy: timestamp,
    orderDirection: desc
  ) {
    timestamp
    ohmCirculatingSupply
  }
}
'''

# Set the headers and query variables for the GraphQL request
headers = {'Content-Type': 'application/json'}

# Send the GraphQL request and extract the data
response = requests.post(url, json={
  'query': query,
}, headers=headers)
data = response.json()['data']['protocolMetrics']

# Convert the data to a pandas DataFrame and group by date, taking the latest value for each day
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df.set_index('timestamp', inplace=True)
df = df.groupby(pd.Grouper(freq='D')).last()

# Save the data to a CSV file
df.to_csv('ohm_circulating_supply.csv', header=['Circulating Supply'])
