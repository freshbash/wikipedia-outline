from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allow only GET requests
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_wikipedia_outline(country: str = Query(..., description="Country name")):

    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Could not fetch Wikipedia page"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    outline = ""
    
    for heading in headings:
        level = int(heading.name[1])  # Extract heading level (1-6)
        outline += "#" * level + " " + heading.get_text(strip=True) + "\n\n"
    
    return {"markdown": outline}
