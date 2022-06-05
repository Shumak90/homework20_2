import pytest
from unittest.mock import MagicMock

from dao.model.movie import Movie
from service.movie import MovieService
from dao.movie import MovieDAO
from conftest import pytest_make_parametrize_id


@pytest.fixture()
def movies_dao():
    movies_dao = MovieDAO(None)
    test_movie = Movie(
        id=1,
        title='title_test',
        description='description_test',
        trailer='trailer_test',
        year=1990,
        rating=5.5
    )
    test_movie2 = Movie(
        id=2,
        title='title_test',
        description='description_test',
        trailer='trailer_test',
        year=1991,
        rating=6.6
    )

    movies_dao.get_one = MagicMock(return_value=test_movie)
    movies_dao.get_all = MagicMock(return_value=[test_movie, test_movie2])
    movies_dao.create = MagicMock(return_value=Movie(id=3))
    movies_dao.update = MagicMock()
    movies_dao.delete = MagicMock()

    return movies_dao

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movies_service(self, movies_dao):
        self.movies_service = MovieService(dao=movies_dao)

    def test_get_one(self):
        movie = self.movies_service.get_one(1)
        assert movie is not None, "movie is not None"
        assert movie.id is not None, "movie.id is not None"

    def test_get_all(self):
        movies = self.movies_service.get_all()
        assert len(movies) > 0, "len(movies) > 0"

    def test_create(self):
        movies_d = {
            'title': 'title_test',
            'description': 'description_test',
            'trailer': 'trailer_test',
            'year': 1993,
            'rating': 7.7
        }
        movie = self.movies_service.create(movies_d)
        assert movie.id is not None, 'movie.id is not None'

    def test_delete(self):
        self.movies_service.delete(1)
        self.movies_service.dao.delete.assert_called_once_with(1)

    def test_update(self):
        movies_d = {
            "id": 3,
            'title': 'title_test',
            'description': 'description_test',
            'trailer': 'trailer_test',
            'year': 1993,
            'rating': 7.7
            }
        self.movies_service.update(movies_d)
        self.movies_service.dao.update.assert_called_once_with(movies_d)