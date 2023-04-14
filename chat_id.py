class ChatIDSingleton:
    __instance = None
    chat_id = None

    def __new__(cls):
        if ChatIDSingleton.__instance is None:
            ChatIDSingleton.__instance = object.__new__(cls)
        return ChatIDSingleton.__instance

    def set_chat_id(self, chat_id):
        ChatIDSingleton.chat_id = chat_id

    def get_chat_id(self):
        return ChatIDSingleton.chat_id