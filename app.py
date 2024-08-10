from openai import OpenAI

client = OpenAI()

if __name__ == '__main__':
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content":
                 "You are a stoic assistant, skilled answers every question with a flare of philosophy on life and death."},
            {"role": "user", "content": "What is python and what it is used for?"}
        ]
    )

    print(completion.choices[0].message)
