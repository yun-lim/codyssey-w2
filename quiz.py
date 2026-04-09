"""Quiz and QuizGame classes for the console quiz game."""

import json
import os
import random
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state.json')


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
