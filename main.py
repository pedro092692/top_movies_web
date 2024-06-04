from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from database import Database, Movie
from forms import EditForm, MovieForm
from get_movie_data import GetMovieData


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap5(app)
movies = GetMovieData()

# CREATE DB
data = Database(app=app)
data.base.init_app(app)

# CREATE TABLE
data.create_table()


@app.route("/")
def home():
    all_movies = data.get_all()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    movie_id = request.args.get('movie_id')
    movie_rating = request.args.get('rating')
    movie_review = request.args.get('review')

    form = EditForm()

    if request.method == 'GET':
        form.rating.data = movie_rating
        form.review.data = movie_review

    if form.validate_on_submit():
        rating = float(form.rating.data)
        review = form.review.data
        data.update(movie_id=movie_id, rating=rating, review=review)
        return redirect(url_for('home'))

    return render_template('edit.html', form=form)


@app.route('/delete')
def delete():

    movie_id = request.args.get('movie_id')
    data.delete(Movie, movie_id)

    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = MovieForm()

    if form.validate_on_submit():
        movies_list_ = movies.search_movie_info(form.title.data)
        if not movies_list_:
            form.title.errors.append(f'No movies with the "{form.title.data}" please try another keyword.')
        else:
            return render_template('add.html', form=form, movies=movies_list_)

    movies_list_ = []
    return render_template('add.html', form=form, movies=movies_list_)


@app.route('/add-movie/<int:movie_id>', methods=['GET', 'POST'])
def add_movie(movie_id):

    movie_details = movies.get_details(movie_id)

    if movie_details:
        new_movie = data.add_movie(
            movie_id=movie_id,
            title=movie_details['title'],
            year=movie_details['year'],
            description=movie_details['overview'],
            img=movie_details['img_url']
        )
    return redirect(url_for('edit', movie_id=movie_id))


if __name__ == '__main__':
    app.run(debug=True)
