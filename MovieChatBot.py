import tkinter as tk
from tkinter import messagebox

import requests
import re

API_KEY = "5a427a8747351a7e79b257311eb0a461"


def get_movie_genre(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()

    if "total_results" in data and data["total_results"] > 0:
        movie_id = data["results"][0]["id"]
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(movie_details_url)
        movie_details = response.json()

        genres = movie_details["genres"]
        genre_names = [genre["name"] for genre in genres]
        genre_string = ", ".join(genre_names)

        return genre_string
    else:
        return "Sorry, I couldn't find any information about that movie."


def replace_words(string, words_to_replace):
    pattern = r'\b(?:{})\b'.format('|'.join(words_to_replace))
    replaced_string = re.sub(pattern, '', string)
    return replaced_string


def get_top_rated_movies_n(n):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&sort_by=vote_average.desc"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        movies = data["results"]
        return movies[:n]
    else:
        return []


def get_top_rated_movies():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&sort_by=vote_average.desc"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        movies = data["results"]
        return movies[:5]
    else:
        return []


def extract_title(user_input):
    patterns = read_patterns_from_file(r"pattern.txt")

    for pattern in patterns:
        match = re.match(pattern, user_input, re.IGNORECASE)

        if match and pattern == "^.*(top|best|highest).* (\d+).*rated.*$":
            n = int(match.group(2))
            print(n)
            return n

        if match and pattern == "^(?:Can you tell me|What is) the release date of (?:the movie )?(.+)$":
            movie_title = match.group(1)
            return [movie_title, 'Date']

        if match and pattern == "^(?:Can you tell me|What is) the genre of (?:the movie )?(.+)$":
            movie_title = match.group(1)
            return [movie_title, 'Genre']

        if match and pattern == "^(?:can you tell me|what is|i want to know about the) the rating of the movie (.+)$":
            movie_title = match.group(1)
            return [movie_title, 'Rating']


        if match and pattern == "^.*(top|best|highest) (rated|movies).*$":
            print(1)
            return 'Top_Rated'

        if match:
            words_to_remove = ['the', 'movie', 'tvshow']
            result = replace_words(match.group(1), words_to_remove)
            return result

    return -999


def read_patterns_from_file(filename):
    with open(filename, "r") as file:
        patterns = [line.strip() for line in file]
    return patterns


def send_message():
    user_message = user_entry.get()
    title = extract_title(user_message)
    chat_box.insert(tk.END, "\n")
    chat_box.insert(tk.END, f"[{user_name}]: {user_message}\n", "user")
    movie_details = get_movie_details(title)
    chat_box.insert(tk.END, "\n")
    chat_box.insert(tk.END, f"[Candida]: {movie_details}\n", "bot")
    chat_box.insert(tk.END, "\n")
    user_entry.delete(0, tk.END)


def get_movie_details(movie_name):

    try:
        if isinstance(movie_name, int) and movie_name > 0:
            movies = get_top_rated_movies_n(movie_name)
            if movies:
                movie_titles = [movie["title"] for movie in movies]
                return "\n".join(movie_titles)
    except:
        return "Can You Rephrase Your Question?. I am Not Able to Understand you"
        
    try:
        if movie_name[1] == 'Genre':
            genres = get_movie_genre(movie_name[0])
            return f"The genres of {movie_name[0]} are: {genres}"
    except:
        return "Can You Rephrase Your Question?. I am Not Able to Understand you"


    try:
        if movie_name[1] == "Date":
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name[0]}"
            response = requests.get(search_url)
            data = response.json()

            if data["total_results"] > 0:
                movie_id = data["results"][0]["id"]
                movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
                response = requests.get(movie_details_url)
                movie_details = response.json()

                title = movie_details["title"]
                release_date = movie_details["release_date"]
                x=f"The Release date of the Movie {title} is {release_date}"
                details = x
                return details
            else:
                return "Sorry, I couldn't find any information about that movie"
    except:
        return "Can You Rephrase Your Question?. I am Not Able to Understand you"

    if movie_name[1] == "Rating":
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name[0]}"
        response = requests.get(search_url)
        data = response.json()

        if data["total_results"] > 0:
            movie_id = data["results"][0]["id"]
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            response = requests.get(movie_details_url)
            movie_details = response.json()

            title = movie_details["title"]
            vote_average = movie_details["vote_average"]
            x=f"The Rating of the Movie {title} is {vote_average}"
            details = x
            return details
        else:
            return "Sorry, I couldn't find any information about that movie"

    if movie_name == -999:
        return "Can you rephrase your question properly"



    if movie_name == "Top_Rated":
        movies = get_top_rated_movies()
        if movies:
            movie_titles = [movie["title"] for movie in movies]
            return "\n".join(movie_titles)

    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    data = response.json()

    if data["total_results"] > 0:
        movie_id = data["results"][0]["id"]
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(movie_details_url)
        movie_details = response.json()

        title = movie_details["title"]
        overview = movie_details["overview"]
        x=f"The Overview of the Movie {title} is {overview}"
        details = x
        return details
    else:
        return "Sorry, I couldn't find any information about that movie."

def get_user_name():
    global user_name
    user_name = name_entry.get()
    if user_name.strip() != "":
        start_dialogue.destroy()
        window.deiconify()
        chat_box.insert(tk.END, f"[Candida]: Hello {user_name}! I am Candida, A Movie Chatbot. How may I help you?\n",
                        "bot")
    else:
        messagebox.showinfo("Invalid Name", "Please enter your name.")

window = tk.Tk()
window.title("Chatbot GUI")
window.configure(bg="#202124")
window.withdraw()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
dialogue_width = 300
dialogue_height = 200
dialogue_x = (screen_width - dialogue_width) // 2
dialogue_y = (screen_height - dialogue_height) // 2

start_dialogue = tk.Toplevel(window)
start_dialogue.title("Welcome!")
start_dialogue.geometry(
    f"{dialogue_width}x{dialogue_height}+{dialogue_x}+{dialogue_y}")
start_dialogue.configure(bg="#202124")

name_label = tk.Label(start_dialogue, text="Enter your name:",
                      bg="#202124", fg="white", font=("Arial", 12))
name_label.pack()

name_entry = tk.Entry(start_dialogue, width=30, font=("Arial", 12))
name_entry.pack()

start_button = tk.Button(start_dialogue, text="Start Chatting", command=get_user_name, bg="#4CAF50", fg="white",
                         bd=0, relief=tk.FLAT, width=12, font=("Arial", 12))
start_button.pack(pady=10)

window_width = 500
window_height = 400
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

chat_box = tk.Text(window, width=50, height=20, bg="#282C34", fg="white", padx=0, pady=0, font=("Arial", 12),
                   wrap="word")
chat_box.tag_config("bot", foreground="#4CAF50")
chat_box.tag_config("user", foreground="#3F88C5")
chat_box.pack(fill=tk.BOTH, expand=True)

input_frame = tk.Frame(window, bg="#202124")
input_frame.pack(pady=10)

user_entry = tk.Entry(input_frame, width=40, fg="black", font=("Arial", 12))
user_entry.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#4CAF50", fg="white", bd=0, relief=tk.FLAT,
                        width=8)
send_button.pack(side=tk.LEFT, padx=5)

start_button.config(borderwidth=0, highlightthickness=0,
                    bd=0, pady=0, padx=0, relief=tk.FLAT)
send_button.config(borderwidth=0, highlightthickness=0,
                   bd=0, pady=0, padx=0, relief=tk.FLAT)

window.mainloop()