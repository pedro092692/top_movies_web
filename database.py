from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


# create extension
base = SQLAlchemy(model_class=Base)


# create table
class Movie(base.Model):

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class Database:

    def __init__(self, app):
        self.app = app
        self.base = base

    def get_or_404(self, table, record_id):
        record = self.base.get_or_404(table, record_id)
        return record

    def create_table(self):
        with self.app.app_context():
            self.base.create_all()

    def get_all(self):
        self.add_ranking()
        all_records = self.base.session.execute(self.base.select(Movie).order_by(Movie.ranking.desc())).scalars()
        return all_records

    def update(self, movie_id, rating, review):
        record_to_update = self.base.get_or_404(Movie, movie_id)
        record_to_update.rating = rating
        record_to_update.review = review

        self.base.session.commit()

    def delete(self, table, movie_id):
        record_to_delete = self.get_or_404(table, movie_id)
        self.base.session.delete(record_to_delete)
        self.base.session.commit()

    def add_movie(self, movie_id, title, year, description, img):

        new_movie = Movie(
            id=movie_id,
            title=title,
            year=year,
            description=description,
            img_url=img
        )
        self.base.session.add(new_movie)
        self.base.session.commit()

    def add_ranking(self):
        # rating = Movie.query.filter(Movie.rating.asc()).all()
        movies_by_ratings = self.base.session.execute(self.base.select(Movie).order_by(Movie.rating.asc())).scalars()

        i = 1

        for rating in movies_by_ratings:

            new_ranking = self.get_or_404(Movie, rating.id)
            new_ranking.ranking = i

            i += 1

            self.base.session.commit()








