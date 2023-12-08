import datetime

TOKENS = [
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJyaWdodHJlZV9wYXJ"
    "0bmVyIiwiZmFrZSI6MX0.E-j4P3kYmJzu6LGtEHzeqRSOhjIi0cwsWgjXZ3r0tjo",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJyaWdodHJlZV9wYXJ"
    "0bmVyIiwiZmFrZSI6Mn0.9u1tYTuE8xDe0OQx1aJJFq2ouzPKsfBW9nK-vGvDzbU",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJyaWdodHJlZV9wYXJ"
    "0bmVyIiwiZmFrZSI6M30.QbLWUNN0wJYLUHogH3RDX0jdxP4IaZn7BZb_5Jk61bU",
]

USERNAME = "brightree_partner"
PASSWORD = "7181c33b138c49d68726e6c24d983cd97ba16c6d"


def get_fake_token(username: str, password: str):
    if username != USERNAME or password != password:
        raise PermissionError

    now = datetime.datetime.now()
    if now.hour <= 8:
        return TOKENS[0]
    if (now.hour > 8) and (now.hour <= 16):
        return TOKENS[1]
    if now.hour > 16:
        return TOKENS[2]
