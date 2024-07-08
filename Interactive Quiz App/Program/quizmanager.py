import os.path
import os
import quizparser
import datetime

class QuizManager:
    def __init__(self, quizfolder):
        self.quizfolder = quizfolder
        self.the_quiz = None
        self.quizzes = dict()
        self.results = None
        self.quiztaker = ""

        if not os.path.exists(quizfolder):
            raise FileNotFoundError("The quiz folder doesn't seem to exist!")

        self._build_quiz_list()

    def _build_quiz_list(self):
        dircontents = os.scandir(self.quizfolder)
        for i, f in enumerate(dircontents):
            if f.is_file() and f.name.endswith('.xml'):
                parser = quizparser.QuizParser()
                with open(f.path, 'r') as quiz_file:
                    self.quizzes[i+1] = parser.parse_quiz(quiz_file)

    def list_quizzes(self):
        for k, v in self.quizzes.items():
            print(f"({k}): {v.name}")

    def take_quiz(self, quizid, username):
        if quizid not in self.quizzes:
            raise ValueError(f"Invalid quiz ID: {quizid}")
        self.quiztaker = username
        self.the_quiz = self.quizzes[quizid]
        self.results = self.the_quiz.take_quiz()
        return self.results

    def print_results(self):
        self.the_quiz.print_results(self.quiztaker)

    def save_results(self):
        today = datetime.datetime.now()
        results_dir = os.path.join(self.quizfolder, 'results')
        os.makedirs(results_dir, exist_ok=True)
        filename = os.path.join(results_dir, f"QuizResults_{today.year}_{today.month}_{today.day}.txt")
        n = 1
        while os.path.exists(filename):
            filename = os.path.join(results_dir, f"QuizResults_{today.year}_{today.month}_{today.day}_{n}.txt")
            n += 1
        with open(filename, "w") as f:
            self.the_quiz.print_results(self.quiztaker, f)
