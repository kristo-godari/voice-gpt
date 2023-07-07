import openai


class ConversationEngine:
    def __init__(self, config):
        openai.api_key = config.get_openai_api_key()

    def chat(self, text):
        ai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

        return ai_response["choices"][0]["text"]
