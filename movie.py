import streamlit as st
import requests
import json
import os

# ----------------------------
# OMDb API Key (hardcoded)
# ----------------------------
API_KEY = "YOUR_OMDB_API_KEY"  # Replace with your actual key

# ----------------------------
# Download history
# ----------------------------
HISTORY_FILE = "download_history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_history(title, url):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    history.append({"title": title, "url": url})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# ----------------------------
# OMDb Functions
# ----------------------------
def search_movies(query):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&s={query}"
    r = requests.get(url).json()
    if r.get("Response") == "True":
        return r["Search"]
    return []

def get_movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}"
    r = requests.get(url).json()
    return r

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🎬 Movie Finder & Download Selector")
st.write("Type a movie name to search and select what to download (legal links).")

# Search box
query = st.text_input("Enter movie name or letters")

if query:
    results = search_movies(query)
    if results:
        st.subheader(f"Results for '{query}':")
        for movie in results:
            imdb_id = movie["imdbID"]
            details = get_movie_details(imdb_id)
            
            col1, col2 = st.columns([1,3])
            with col1:
                poster = details.get("Poster")
                if poster and poster != "N/A":
                    st.image(poster, width=120)
            with col2:
                st.write(f"### {details.get('Title')} ({details.get('Year')})")
                st.write(f"**Plot:** {details.get('Plot')}")
                st.write(f"**Rating:** {details.get('imdbRating')}")
                
                # Download button (just saves to history)
                if st.button(f"Download {details.get('Title')}", key=imdb_id):
                    # In real use, replace with a legal source URL
                    download_url = f"https://example.com/download/{imdb_id}"
                    save_history(details.get("Title"), download_url)
                    st.success(f"'{details.get('Title')}' added to download history!")

    else:
        st.warning("No movies found.")

# Download history
st.subheader("📥 Download History")
history = load_history()
if history:
    for h in history:
        st.write(f"**{h['title']}** — {h['url']}")
else:
    st.info("No downloads yet.")
