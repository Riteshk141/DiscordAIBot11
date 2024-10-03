from responses import get_response


class CustomUserResponses:
    def __init__(self,specific_user2):
        self.specific_user2 = specific_user2



    def get_custom_response2(self, username, user_message):
        if username != self.specific_user2:
            return None

        user_message_lower = user_message.lower()
        if "hello" in user_message_lower:
            return "Hi there special user!"
        elif "hi" in user_message_lower:
            return "you\re"
        elif "how are you" in user_message_lower:
            return "I'm doing well, special user. How about you?"
        elif "bye" in user_message_lower:
            return "Goodbye, special user!"
        else:
            return get_response(user_message)
        # Call get_response if the message does not match any custom response





