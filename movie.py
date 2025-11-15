import streamlit as st
import requests
import os
import json



# Load API key
API_KEY = os.getenv("OMDB_API_KEY")

# History file
HISTORY_FILE = "download_history.json"

# Initialize history file if not exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


# Save to download history
def save_history(movie_title, download_url):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    new_entry = {
        "title": movie_title,
        "url": download_url
    }
    history.append(new_entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# Load download history
def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


# Movie Search Function
def search_movie(title):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&s={title}"
    resp = requests.get(url)
    return resp.json()


# Detailed Movie Lookup
def movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}"
    resp = requests.get(url)
    return resp.json()


# UI Starts Here
st.title("🎬 Movie Finder + Download Manager")
st.write("Search for movies and save download history.")


# Search movie
movie_name = st.text_input("Enter movie name")

if movie_name:
    results = search_movie(movie_name)

    if results.get("Response") == "True":
        st.subheader("Search Results:")
        for item in results["Search"]:
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(item.get("Poster"), width=120)

            with col2:
                st.write(f"### {item['Title']} ({item['Year']})")
                movie_data = movie_details(item["imdbID"])

                # Dummy download link (replace with legal sources later)
                download_url = f"https://example.com/download/{item['imdbID']}"

                st.write("**Plot:**", movie_data.get("Plot"))
                st.write("**Rating:**", movie_data.get("imdbRating"))

                # Download Button
                if st.button(f"Download {item['Title']}", key=item["imdbID"]):
                    save_history(item["Title"], download_url)
                    st.success(f"Added '{item['Title']}' to download history!")


# Download History
st.subheader("📥 Download History")

history = load_history()
if history:
    for entry in history:
        st.write(f"**{entry['title']}** — {entry['url']}")
else:
    st.info("No downloads yet.")
