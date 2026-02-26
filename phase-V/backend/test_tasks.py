from sqlmodel import Session, select, create_engine
from models import Task
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
session = Session(engine)

tasks = session.exec(select(Task).where(Task.user_id == 'XyaU8F0PvkbdH3CwBBpV3jRz4EWYcvad')).all()
print(f'Found {len(tasks)} tasks')

for t in tasks:
    print(f'\nTask {t.id}: {t.title}')
    print(f'  Priority: {t.priority}')
    print(f'  Due Date: {t.due_date}')
    print(f'  Has tags attr: {hasattr(t, "tags")}')
    if hasattr(t, 'tags'):
        print(f'  Tags type: {type(t.tags)}')
        print(f'  Tags value: {t.tags}')
