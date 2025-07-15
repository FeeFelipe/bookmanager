import dramatiq

@dramatiq.actor(queue_name="books_updated")
def book_updated_event(book_data: dict):
    print(f"[book_updated_event] Queued event: {book_data['title']}")
