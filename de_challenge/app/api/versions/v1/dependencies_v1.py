from app.database.db_connection import BaseDBModel

# Global Dependencies

def get_db():
    db = BaseDBModel.session_factory()
    try:
        yield db
    finally:
        db.close()