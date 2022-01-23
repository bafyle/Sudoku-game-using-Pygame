CREATE TABLE Quizzes(q_id INTEGER PRIMARY KEY AUTOINCREMENT,
					 quiz TEXT NOT NULL);
CREATE TABLE Answers(a_id INTEGER, answer TEXT NOT NULL,
					 FOREIGN KEY(a_id) REFERENCES Quizzes(q_id) ON DELETE CASCADE);