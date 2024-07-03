import requests
import pandas as pd

# Spotify API credentials
client_id = 'd682731250b745d580eac1915451a9bb'
client_secret = '5791ad7232fb4b8a868de0786f91ead4'

# Authenticate and obtain access token
auth_url = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Headers for Spotify API requests
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Function to fetch cover URL
def get_cover_url(track_name, artist_name):
    search_url = 'https://api.spotify.com/v1/search'
    query = f'track:{track_name} artist:{artist_name}'
    response = requests.get(search_url, headers=headers, params={'q': query, 'type': 'track', 'limit': 1})
    response_data = response.json()
    tracks = response_data.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['album']['images'][0]['url']
    return None

# Load your CSV file
file_path = 'C:/Users/Aryan/Downloads/archive/spotify-2023.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Add a new column for cover URLs
df['cover_url'] = df.apply(lambda row: get_cover_url(row['track_name'], row['artist(s)_name']), axis=1)

# Save the updated DataFrame back to a CSV file
df.to_csv('spotify-2023-with-covers.csv', index=False, encoding='ISO-8859-1')
