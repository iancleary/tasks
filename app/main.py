import datetime
from typing import Union

import database

from fastapi import FastAPI

app = FastAPI()

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.
Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")

    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title=title, release_timestamp=timestamp)

def print_movie_list(heading, movies):
    print(f"---{heading} Movies---")
    for movie in movies:
        release_date = datetime.datetime.fromtimestamp(movie[1])
        human_date = release_date.strftime("%b %d %Y")
        print(f"{movie[0]} (on {human_date})")
    print("---- \n")


def prompt_watch_movie():
    movie_title = input("Enter movie title you've watched: ")
    database.watch_movie(title=movie_title)

# while (user_input := input(menu)) != "6":
#     if user_input == "1":
#         prompt_add_movie()
#     elif user_input == "2":
#         movies = database.get_movies(upcoming=True)
#         print_movie_list("Upcoming", movies)
#     elif user_input == "3":
#         movies = database.get_movies(upcoming=False)
#         print_movie_list("All", movies)
#     elif user_input == "4":
#         prompt_watch_movie()
#     elif user_input == "5":
#         movies = database.get_watched_movies()
#         print_movie_list("Watched", movies)
#     else:
#         print("Invalid input, please try again!")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
