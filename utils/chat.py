

def instruct_openai(user_message: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": translation_prompt},
            {"role": "user", "content": transcript}
        ],
    )

    return response.choices[0].message.content