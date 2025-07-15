import dramatiq

@dramatiq.actor(queue_name="books_created")
def book_created_event(book_data: dict):
    print(f"[book_created_event] Queued event: {book_data['title']}")
