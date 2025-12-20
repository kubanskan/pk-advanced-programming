from sqlalchemy.orm import Session
from typing import List, Sequence
from .models import ForbiddenWord
from sqlalchemy import select

class ForbiddenWordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> Sequence[ForbiddenWord]:
        print(type(self.db.query(ForbiddenWord).all() ))
        return self.db.scalars(select(ForbiddenWord)).all()

    def get_all_words(self) -> List[str]:
        words = self.db.query(ForbiddenWord.word).all()
        return [word[0].lower() for word in words]

    def add(self, word: str) -> ForbiddenWord:
        forbidden_word = ForbiddenWord(word=word.lower(), )
        self.db.add(forbidden_word)
        self.db.commit()
        self.db.refresh(forbidden_word)
        return forbidden_word

    def delete(self, word_id: int) -> int:
        deleted = self.db.query(ForbiddenWord).filter(
            ForbiddenWord.id == word_id
        ).delete()
        self.db.commit()
        return deleted
