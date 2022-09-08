from game_items.game_objects import GameObject, _set_last_id, SAMPLE_GAME_OBJECT
import sqlite3
import pickle


class GameBase:
    def __init__(self, base_name: str, collection_name: str) -> None:
        self._base_name = base_name
        self._collection_name = collection_name
        self.game_objects_list: list[GameObject] = []
        self.collection_list: list[GameObject] = []
        self._connect_to_base()
        self._connect_to_collection()
        self.target_game_objects: list[GameObject] = []
        self.bufer_game_objects: list[GameObject] = []

    def _connect_to_base(self):
        self.con = sqlite3.connect(self.base_name)
        self.cur = self.con.cursor()
        self.con.execute(
            '''CREATE TABLE IF NOT EXISTS game_objects (id INTEGER, game_object BLOB);''')
        self.cur.execute('''SELECT * FROM game_objects;''')
        for row in self.cur.fetchall():
            self.game_objects_list.append(pickle.loads(row[1]))
        self._update_last_id()

    def _connect_to_collection(self):
        self.collection_con = sqlite3.connect(self.collection_name)
        self.collection_cur = self.collection_con.cursor()
        self.collection_con.execute(
            '''CREATE TABLE IF NOT EXISTS collection (id INTEGER, game_object BLOB);''')
        self.collection_cur.execute('''SELECT * FROM collection;''')
        for row in self.collection_cur.fetchall():
            self.collection_list.append(pickle.loads(row[1]))
        if len(self.game_objects_list) == 0:
            g = SAMPLE_GAME_OBJECT
            self.add_game_objects(g)

    def _update_last_id(self):
        max_id = -1
        for g in self.game_objects_list:
            if g.id > max_id:
                max_id = g.id
        _set_last_id(max_id)

    def exit(self):
        self.cur.close()
        self.con.close()
        self.collection_cur.close()
        self.collection_con.close()

    @property
    def game_objects(self):
        return self.game_objects_list

    @property
    def target(self):
        return self.target_game_objects

    @target.setter
    def target(self, n):
        self.target_game_objects = n

    @property
    def bufer(self):
        return self.bufer_game_objects

    @bufer.setter
    def bufer(self, n):
        self.bufer_game_objects = n

    @property
    def collection(self):
        return self.collection_list

    @property
    def collection_name(self):
        return self._collection_name

    @property
    def base_name(self):
        return self._base_name

    def add_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.game_objects_list.append(game_object)
            self.con.execute(
                '''INSERT INTO game_objects VALUES (?, ?);''', (game_object.id, pickle.dumps(game_object)))
            self.con.commit()

    def update_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.con.execute('''UPDATE game_objects SET game_object = ? WHERE id = ?;''',
                             (pickle.dumps(game_object), game_object.id))
            self.con.commit()

    def remove_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.game_objects_list.remove(game_object)
            self.con.execute(
                '''DELETE FROM game_objects WHERE id = ?;''', (game_object.id, ))
            self.con.commit()

    def find_game_object_from_id(self, id):
        # TODO: доработать с помощью алгоритма
        for g in self.game_objects_list:
            if g.id == id:
                return g
        return None

    def add_collection_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.collection_list.append(game_object)
            self.collection_con.execute(
                '''INSERT INTO collection VALUES (?, ?);''', (game_object.id, pickle.dumps(game_object)))
            self.collection_con.commit()

    def update_collection_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.collection_con.execute(
                '''UPDATE collection SET game_object = ? WHERE id = ?;''', (pickle.dumps(game_object), game_object.id))
            self.collection_con.commit()

    def remove_collection_game_objects(self, *game_objects):
        for game_object in game_objects:
            self.collection_list.remove(game_object)
            self.collection_con.execute(
                '''DELETE FROM collection WHERE id = ?;''', (game_object.id, ))
            self.collection_con.commit()

    def find_collection_game_object_from_id(self, id):
        # TODO: доработать с помощью алгоритма
        for g in self.collection_list:
            if g.id == id:
                return g
        return None
