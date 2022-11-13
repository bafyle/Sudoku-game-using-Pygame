import sqlite3

class Database:
    """
    Connects to sqlite database in read-only mode by passing
    the database path in string
    """
    def __init__(self, db_path: str):
        self.database_path = db_path

        connection_query = rf"file:{self.database_path}?mode=ro"
        Database.connection = sqlite3.connect(connection_query, uri = True)

        self.cursor = Database.connection.cursor()

    
    def get_number_of_puzzles(self) -> int:
        """
        Return the number of puzzles in the database
        """
        data = self.cursor.execute("Select count(quiz) from Quizzes")
        return data.fetchone()[0]

    
    def get_puzzle_string(self, id: int) -> str:
        """
        This function reads a puzzle from the database and returns 
        it in string foramt
        """
        data = self.cursor.execute("SELECT quiz FROM Quizzes WHERE q_id = ?", [id])

        """
            Since the q_id is a primary key in the database,
            there will be only one object in 'puzzleText'
            we get that object and reassign 'puzzleText' with it
            for i in puzzle_text:
                puzzle_text = i
            puzzle_text = puzzle_text[0]
        """
        return data.fetchone()[0]
    
    def get_answer_string(self, id: int) -> str:
        """
        This functions reads the answer of a certain puzzle and
        returns it in string format
        """
        answer_text = self.cursor.execute("SELECT quiz FROM Answers WHERE a_id = ?", [id])

        return answer_text.fetchone()[0]
    
    @classmethod
    def close_connection(cls):
        Database.connection.close()
    
    @classmethod
    def close_connection_commit(cls):
        Database.connection.commit()
        Database.close_connection()
