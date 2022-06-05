import pytest
from unittest.mock import MagicMock

from dao.model.genre import Genre
from service.genre import GenreService
from dao.genre import GenreDAO
from conftest import pytest_make_parametrize_id


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)
    test_genre = Genre(
        id=1,
        name="test"
    )
    test_genre2 = Genre(
        id=2,
        name="tast2"
    )

    genre_dao.get_one = MagicMock(return_value=test_genre)
    genre_dao.get_all = MagicMock(return_value=[test_genre, test_genre2])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.update = MagicMock()
    genre_dao.delete = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genres_service(self, genre_dao):
        self.genres_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genres_service.get_one(1)
        assert genre is not None, "genre is not None"
        assert genre.id is not None, "genre.id is not None"

    def test_get_all(self):
        genres = self.genres_service.get_all()
        assert len(genres) > 0, "len(genres) > 0"

    def test_create(self):
        genre_d = {
            'title': 'title_test',
            'description': 'description_test',
            'trailer': 'trailer_test',
            'year': 1993,
            'rating': 7.7
        }
        genre = self.genres_service.create(genre_d)
        assert genre.id is not None, 'movie.id is not None'

    def test_delete(self):
        self.genres_service.delete(1)
        self.genres_service.dao.delete.assert_called_once_with(1)

    def test_update(self):
        genre_d = {
            "id": 3,
            'title': 'title_test',
            'description': 'description_test',
            'trailer': 'trailer_test',
            'year': 1993,
            'rating': 7.7
            }
        self.genres_service.update(genre_d)
        self.genres_service.dao.update.assert_called_once_with(genre_d)

