class Logger:

    def log(self, text, **data):
        if "message" in data:
            print(f"User {data.get('message').from_user.id} ", end="")
        print(text, data)

