from datetime import datetime

from beanie import Document, before_event, ValidateOnSave


class Base(Document):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @before_event(ValidateOnSave)
    def update_time(self):
        updated_at = datetime.now()
