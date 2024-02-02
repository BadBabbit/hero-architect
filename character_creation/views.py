from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
from django.http import HttpResponse


class OpenAIClient:
    load_dotenv()
    client = OpenAI()

    @staticmethod
    def get_client():
        return OpenAIClient.client

def openAI_API_call(client, messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message


def index_view(request):
    data = {}
    return render(request, 'index_view.html', data)

def main():
    client = OpenAIClient.get_client()
    messages = [
            {
                "role": "system",
                "content": "You are just kinda happy to be here."},
            {
                "role": "user",
                "content": "Yooo dude, how ya feelin the vibes of this place?"}
        ]
    print(openAI_API_call(client, messages))


if __name__ == "__main__":
    main()

