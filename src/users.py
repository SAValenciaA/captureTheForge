import uuid
import hashlib
import database

md5 = lambda password: hashlib.md5(password.encode()).hexdigest()

class User:
    def __init__(self, user_data):

        self.formatted = lambda v: str(v) if type(v) == int else f"'{v}'"

        self.values_names_list = ['id', 'name', 'score', 'password', 'solves', 'teamID']

        self.id = user_data['id']
        self.name = user_data['name']
        self.score = user_data['score']
        self.password = user_data['password']
        self.solves = user_data['solves']
        self.teamID = user_data['teamID']

        self.values = lambda: [self.id, self.name, self.score, self.password, self.solves, self.teamID]

        self.values_pair = lambda: zip(self.values_names_list, self.values())

    def save(self, scoreboard):

        values_changed = ", ".join(value[0] + " = " + self.formatted(value[1]) for value in self.values_pair())
        query = f"update Users set {values_changed} where id == '{self.id}'"
        print(query)

        database.insert(query)

        scoreboard.delete(self.name)
        scoreboard.insert(self)


    @staticmethod
    def create_user(name:str, password: str, teamID: str):

        formatted = lambda v: str(v) if type(v) == int else f"'{v}'"

        id = str(uuid.uuid4())
        score = 0
        solves = ""
        password = md5(password)

        values_names_list = ['id', 'name', 'score', 'password', 'solves', 'teamID']
        values_names = ", ".join(values_names_list)

        initial_values_list = [id, name, score, password, solves, teamID]
        initial_values = ", ".join(formatted(i) for i in initial_values_list)

        insert_query = f"insert into Users ({values_names}) values ({initial_values})"
        print(insert_query)

        database.insert(insert_query)


    @staticmethod
    def get_user(search_criteria: str, value):
        search_value = f'{value}' if type(value) == int else f"'{value}'"
        search_query = f"select * from Users where {search_criteria} == {search_value}"
        user_data = database.query(search_query, one=True)
        if user_data == None:
            return None
        user = User(user_data)
        return user
    

class Node:
    def __init__(self, user):
        self.user = user
        self.next = None

class ScoreBoard:
    MAX_SIZE = 50

    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, user):
        new_node = Node(user)

        if not self.head:
            self.head = new_node
            self.size = 1
            return

        if user.score > self.head.user.score:
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            self._ensure_max_size()
            return

        current = self.head
        while current.next and current.next.user.score >= user.score:
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1

        self._ensure_max_size()

    def _ensure_max_size(self):
        """Elimina al usuario con peor score si hay más de 50."""
        if self.size <= self.MAX_SIZE:
            return

        current = self.head
        while current.next and current.next.next:
            current = current.next

        current.next = None
        self.size -= 1

    def find(self, name):
        current = self.head
        while current:
            if current.user.name == name:
                return current.user
            current = current.next
        return None

    def delete(self, name):
        current = self.head
        while current.next:
            if current.next.user.name == name:
                current.next = current.next.next
                break
            current = current.next

    def print_list(self):
        current = self.head
        index = 1
        while current:
            print(f"{index}. {current.user}")
            current = current.next
            index += 1

    def __iter__(self):
        current = self.head
        while current:
            yield current.user
            current = current.next

