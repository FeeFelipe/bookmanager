import dramatiq

@dramatiq.actor(queue_name="books_deleted")
def book_deleted_event(book_data: dict):
    print(f"[book_deleted_event] Queued event: {book_data['title']}")
