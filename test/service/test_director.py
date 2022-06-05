import pytest
from unittest.mock import MagicMock

from dao.model.director import Director
from service.director import DirectorService
from dao.director import DirectorDAO


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    test_director = Director(
        id=1,
        name="test"
    )
    test_director2 = Director(
        id=2,
        name="tast2"
    )

    director_dao.get_one = MagicMock(return_value=test_director)
    director_dao.get_all = MagicMock(return_value=[test_director, test_director2])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()

    return director_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.directors_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.directors_service.get_one(1)
        assert director is not None, "director is not None"
        assert director.id is not None, "director.id is not None"

    def test_get_all(self):
        directors = self.directors_service.get_all()
        assert len(directors) > 0, "len(directors) > 0"

    def test_create(self):
        director_d = {
            'name': "tast2"
        }
        director = self.directors_service.create(director_d)
        assert director.id is not None, 'movie.id is not None'

    def test_delete(self):
        self.directors_service.delete(1)
        self.directors_service.dao.delete.assert_called_once_with(1)

    def test_update(self):
        director_d = {
            "id": 3,
            'name': "tast2"
            }
        self.directors_service.update(director_d)
        self.directors_service.dao.update.assert_called_once_with(director_d)

