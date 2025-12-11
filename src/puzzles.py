import uuid
import hashlib
import database

md5 = lambda password: hashlib.md5(password.encode()).hexdigest()

class Puzzle:
    def __init__(self, puzzle_data):

        self.id = puzzle_data['id']
        self.name = puzzle_data['name']
        self.tags = puzzle_data['tags']
        self.flag = puzzle_data['flag']
        self.description = puzzle_data['description']
        self.extraFiles = puzzle_data['extraFiles']
        self.dificulty = puzzle_data['dificulty']


    @staticmethod
    def create_puzzle(name:str, flag: str, tags: str, description: str, extraFiles: str, dificulty: int):

        formatted = lambda v: str(v) if type(v) == int else f"'{v}'"

        id = str(uuid.uuid4())
        flag = md5(flag)

        values_names_list = ['id', 'name', 'flag', 'tags', 'description', 'extraFiles', 'dificulty']
        values_names = ", ".join(values_names_list)

        initial_values_list = [id, name, flag, tags, description, extraFiles, dificulty]
        initial_values = ", ".join(formatted(i) for i in initial_values_list)

        insert_query = f"insert into Puzzles ({values_names}) values ({initial_values})"
        print(insert_query)

        database.insert(insert_query)


    @staticmethod
    def get_puzzle(search_criteria: str, value):
        search_value = f'{value}' if type(value) == int else f"'{value}'"
        search_query = f"select * from Puzzles where {search_criteria} == {search_value}"
        puzzle_data = database.query(search_query, one=True)
        if puzzle_data == None:
            return None
        puzzle = Puzzle(puzzle_data)
        return puzzle

    @staticmethod
    def get_puzzle_list():
        search_query = 'select * from Puzzles limit 30'
        puzzles = database.query(search_query)
        return puzzles

