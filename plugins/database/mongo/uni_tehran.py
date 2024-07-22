from database.mongo.basic import MongoBasic


UNI_TEHRAN = "UNI_TEHRAN"
CURSORS = f"{UNI_TEHRAN}_CURSORS"


class UniTehran(MongoBasic):

    def __init__(self, database_name: str = None) -> None:
        super().__init__(database_name)

    def save_page(self, search_type: str, page: int):
        self.db[CURSORS].update_one({'search_type': search_type}, {'$set': {'search_type': search_type, 'page': page}}, upsert=True)

    def load_page(self, search_type: str, use_cache: bool) -> int:
        if use_cache:
            cursor = self.db[CURSORS].find_one({'search_type': search_type})
            if cursor:
                return cursor.get('page')
            else:
                return 1
        else:
            return 1

    def delete_page(self, search_type: str):
        self.db[CURSORS].delete_one({'search_type': search_type})

    def save_cursor(self, college: str, cursor: int):
        self.db[CURSORS].update_one({'college': college}, {'$set': {'college': college, 'cursor': cursor}}, upsert=True)

    def load_cursor(self, college: str, use_cache: bool) -> int:
        if use_cache:
            cursor = self.db[CURSORS].find_one({'college': college})
            if cursor:
                return cursor.get('cursor')
            else:
                return 1
        else:
            return 1

    def delete_cursor(self, college: str):
        self.db[CURSORS].delete_one({'college': college})


mongo_tehran = UniTehran()
