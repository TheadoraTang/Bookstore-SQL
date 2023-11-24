import pytest

from fe.access.new_seller import register_new_seller
import uuid
import time


class TestCreateStore:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_create_store_user_{}".format(time.time())
        self.store_id = "test_create_store_store_{}".format(time.time())
        self.password = self.user_id
        yield

    def test_ok(self):
        self.seller = register_new_seller(self.user_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200

    def test_error_exist_store_id(self):
        self.seller = register_new_seller(self.user_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200

        code = self.seller.create_store(self.store_id)
        assert code != 200
