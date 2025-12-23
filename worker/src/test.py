from spotify_scraper import SpotifyClient

# Initialize client with rate limiting (default 0.5s between requests)
client = SpotifyClient()

# Get playlist details
playlist = client.get_playlist_info(
    "https://open.spotify.com/playlist/37i9dQZF1DX0Yxoavh5qJV"
)

print(f"Tracks: {playlist.get('track_count', 0)}")

# Get all tracks
for track in playlist["tracks"]:
    print(
        f"  - {track.get('name', 'Unknown')} by {(track.get('artists', [{}])[0].get('name', 'Unknown') if track.get('artists') else 'Unknown')}"
    )
