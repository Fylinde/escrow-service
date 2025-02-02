def send_notification(user_id: int, message: str):
    # Integrate RabbitMQ or WebSocket here
    print(f"Notification sent to user {user_id}: {message}")
