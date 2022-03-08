import sqlite3

class Database:
    """
    Connects to sqlite database in read-only mode by passing
    the database path in string
    """
    def __init__(self, dbpath: str):
        self.database_path = dbpath

        connection_query = rf"file:{self.database_path}?mode=ro"
        Database.connection = sqlite3.connect(connection_query, uri = True)

        self.cursor = Database.connection.cursor()
    
    def get_puzzle_string(self, id: int) -> str:
        """
        This function reads a puzzle from the database and returns 
        it in string foramt
        """
        puzzle_text = self.cursor.execute("SELECT quiz FROM Quizzes WHERE q_id = ?", [id])

        """
            Since the q_id is a primary key in the database,
            there will be only one object in 'puzzleText'
            we get that object and reassign 'puzzleText' with it
            for i in puzzle_text:
                puzzle_text = i
            puzzle_text = puzzle_text[0]
        """

        for row in puzzle_text:
            return row[0]
    
    def get_answer_string(self, id: int) -> str:
        """
        This functions reads the answer of a certain puzzle and
        returns it in string format
        """
        answer_text = self.cursor.execute("SELECT quiz FROM Answers WHERE a_id = ?", [id])

        for i in answer_text:
            answer_text = i
        answer_text = answer_text[0]

        return answer_text
    
    @classmethod
    def close_connection(cls):
        Database.connection.close()
    
    @classmethod
    def close_connection_commit(cls):
        Database.connection.commit()
        Database.close_connection()
