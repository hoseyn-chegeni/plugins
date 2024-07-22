from .basic import MongoBasic


UNI_BEHESHTI = "UNI_BEHESHTI"
UNI_BEHESHTI_CURSORS = f"{UNI_BEHESHTI}_CURSORS"


class Beheshti(MongoBasic):

    def __init__(self, database_name: str = None) -> None:
        super().__init__(database_name)

    def save_page(self, page: int):
        self.db[UNI_BEHESHTI_CURSORS].update_one({}, {'$set': {'page': page}}, upsert=True)

    def load_page(self, use_cache: bool) -> int:
        if use_cache:
            cursor = self.db[UNI_BEHESHTI_CURSORS].find_one({})
            if cursor:
                return cursor.get('page')
            else:
                return 1
        else:
            return 1

    def delete_page(self):
        self.db[UNI_BEHESHTI_CURSORS].delete_one({})


mongo_beheshti = Beheshti()