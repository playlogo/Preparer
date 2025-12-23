from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/playlist")
def api_response():
    return "https://open.spotify.com/playlist/37i9dQZF1DX0Yxoavh5qJV"


app.mount("/", StaticFiles(directory="html", html=True), name="html")
