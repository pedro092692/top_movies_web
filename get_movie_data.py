import requests

url_list = 'https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNGEzYjM0OThkMmM5N2QzMTM5MDczYTc3NmJhMjc3NCIsInN1YiI6IjY1YzUzNT\
IwYmQ1ODhiMDE2MzQ0NzU2YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CpJPYisBNPkh5GpquE-XDtpiJX8Au8RH1mBtaEuBUEk'


class GetMovieData:

    def __init__(self):
        self.url_list = url_list
        self.token = token

        self.headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {self.token}"
        }

    def search_movie_info(self, query):
        response = requests.get(self.url_list, headers=self.headers, params={"query": query})
        movies = response.json()
        movies_titles = movies['results']

        movies_info = [{"movie_title": movie['title'],
                        "movie_release_date": movie['release_date'][0:4],
                        "movie_id": movie['id']}
                        for movie in movies_titles]

        return movies_info

    def get_details(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=self.headers)
        details = response.json()

        try:
            movie_details = {
                "title": details['title'],
                "overview": details['overview'],
                "year": details['release_date'][0:4],
                "img_url": f"https://image.tmdb.org/t/p/w500{details['poster_path']}"
                }

        except KeyError:
            return False

        return movie_details





