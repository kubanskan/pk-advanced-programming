from src.repository.database import SessionLocal
from src.repository.forbidden_word_repository import ForbiddenWordRepository


def seed_forbidden_words():
    db = SessionLocal()
    try:
        repo = ForbiddenWordRepository(db)
        forbidden_words_data = ['spam', 'fake', 'scam', 'illegal']

        for word in forbidden_words_data:
            repo.add(word)


    except Exception as e:
        print(f'Error: {e}')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    seed_forbidden_words()
