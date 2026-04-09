"""Quiz and QuizGame classes for the console quiz game."""

import json
import os
import random
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state.json')

DEFAULT_QUIZZES = [
    {
        'question': 'Python에서 리스트의 마지막 요소를 가져오는 인덱스는?',
        'choices': ['0', '-1', 'last', 'end'],
        'answer': 2,
        'hint': '음수 인덱스를 사용하면 뒤에서부터 접근할 수 있습니다.'
    },
    {
        'question': 'Python에서 딕셔너리를 생성하는 올바른 방법은?',
        'choices': ['[1, 2, 3]', '(1, 2, 3)', "{'key': 'value'}", '<1, 2, 3>'],
        'answer': 3,
        'hint': '중괄호 {}를 사용하며, key: value 형태로 작성합니다.'
    },
    {
        'question': "다음 중 Python의 내장 함수가 아닌 것은?",
        'choices': ['len()', 'print()', 'input()', 'scan()'],
        'answer': 4,
        'hint': 'C언어에서 입력받을 때 사용하는 함수와 이름이 비슷합니다.'
    },
    {
        'question': 'Python에서 여러 줄 문자열을 만들 때 사용하는 것은?',
        'choices': ["작은따옴표 '", '큰따옴표 "', "삼중따옴표 '''", '백틱 `'],
        'answer': 3,
        'hint': '따옴표를 세 번 연속으로 사용합니다.'
    },
    {
        'question': 'Python에서 모듈을 가져올 때 사용하는 키워드는?',
        'choices': ['include', 'require', 'import', 'using'],
        'answer': 3,
        'hint': '영어로 "수입하다"라는 뜻을 가진 단어입니다.'
    },
    {
        'question': 'Python의 for 문에서 0부터 4까지 반복하려면?',
        'choices': ['for i in range(4)', 'for i in range(5)', 'for i in range(1, 5)', 'for i in 0..4'],
        'answer': 2,
        'hint': 'range(n)은 0부터 n-1까지의 숫자를 생성합니다.'
    },
    {
        'question': 'Python에서 예외 처리를 위해 사용하는 구문은?',
        'choices': ['if/else', 'try/except', 'switch/case', 'do/while'],
        'answer': 2,
        'hint': '시도(try)하고 예외(except)를 잡는 구문입니다.'
    },
]


class Quiz:
    """Represents a single quiz question with choices and an answer."""

    def __init__(self, question, choices, answer, hint=''):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number=None):
        """Display the quiz question and choices."""
        if number is not None:
            print(f'\n    [문제 {number}]')
        print(f'    {self.question}\n')
        for i, choice in enumerate(self.choices, 1):
            print(f'    {i}. {choice}')

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        return user_answer == self.answer

    def to_dict(self):
        """Convert quiz to dictionary for JSON serialization."""
        data = {
            'question': self.question,
            'choices': self.choices,
            'answer': self.answer,
        }
        if self.hint:
            data['hint'] = self.hint
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Quiz instance from a dictionary."""
        return cls(
            question=data['question'],
            choices=data['choices'],
            answer=data['answer'],
            hint=data.get('hint', ''),
        )


class QuizGame:
    """Manages the entire quiz game: menu, play, add, list, score, save/load."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.score_history = []
        self.load_data()

    def load_data(self):
        """Load quiz data from state.json. Use defaults if missing or corrupted."""
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get('quizzes', [])]
            self.best_score = data.get('best_score', None)
            self.score_history = data.get('score_history', [])
            count = len(self.quizzes)
            score_info = f', 최고점수 {self.best_score}점' if self.best_score is not None else ''
            print(f'    저장된 데이터를 불러왔습니다. (퀴즈 {count}개{score_info})')
        except FileNotFoundError:
            self._load_defaults()
            print('    저장 파일이 없어 기본 퀴즈 데이터를 사용합니다.')
        except (json.JSONDecodeError, KeyError, TypeError):
            self._load_defaults()
            print('    저장 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.')

    def _load_defaults(self):
        """Load default quiz data."""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = None
        self.score_history = []

    def save_data(self):
        """Save quiz data to state.json."""
        data = {
            'quizzes': [q.to_dict() for q in self.quizzes],
            'best_score': self.best_score,
            'score_history': self.score_history,
        }
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f'\n    저장 중 오류가 발생했습니다: {e}')

    def _get_number_input(self, prompt, min_val, max_val):
        """Get validated number input from user within range."""
        while True:
            try:
                raw = input(prompt).strip()
                if not raw:
                    print(f'    입력이 비어 있습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
                    continue
                num = int(raw)
                if num < min_val or num > max_val:
                    print(f'    잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
                    continue
                return num
            except ValueError:
                print(f'    잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')

    def _get_text_input(self, prompt):
        """Get non-empty text input from user."""
        while True:
            raw = input(prompt).strip()
            if raw:
                return raw
            print('    입력이 비어 있습니다. 다시 입력하세요.')

    def show_menu(self):
        """Display the main menu."""
        print('\n    ========================================')
        print('            나만의 퀴즈 게임')
        print('    ========================================')
        print('    1. 퀴즈 풀기')
        print('    2. 퀴즈 추가')
        print('    3. 퀴즈 목록')
        print('    4. 점수 확인')
        print('    5. 퀴즈 삭제')
        print('    6. 종료')
        print('    ========================================')

    def run(self):
        """Main game loop."""
        try:
            while True:
                self.show_menu()
                choice = self._get_number_input('    선택: ', 1, 6)

                if choice == 6:
                    self.save_data()
                    print('\n    게임을 종료합니다. 안녕히 가세요!')
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_data()
            print('\n\n    프로그램을 안전하게 종료합니다.')
