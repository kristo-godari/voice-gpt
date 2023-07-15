import openai
from retry import retry


class ConversationEngine:
    def __init__(self, config):
        openai.api_key = config.get_openai_api_key()

    @retry(Exception, tries=3, delay=0)
    def chat(self, text):
        print(f"Started calling OpenAPi with the following text: \n {text} \n")
        try:
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

            response = ai_response["choices"][0]["text"]
        except Exception as e:
            print(e)
            response = "Quota exceed"

        print(f"Response from OpenApi is: \n {response} \n")

        return response