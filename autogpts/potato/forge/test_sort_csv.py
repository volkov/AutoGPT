import openai
import json


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = ("Sort the input.csv by the 'timestamp' column and write the new csv in the output.csv file. "
            "The order of the columns should be preserved.")
    file_content = ("id,name,timestamp"
                    "3,Alice,2023-09-25 14:10:00"
                    "1,Bob,2023-09-24 12:05:00"
                    "2,Charlie,2023-09-24 12:10:00"
                    "4,David,2023-09-26 16:20:00")
    print("#####")
    print("Task:")
    print(task)

    model = "gpt-3.5-turbo-0613"
    #model = "gpt-4-0613"

    print()
    print()
    print('############')
    print("Model talks:")
    talk_messages = [{"role": "user", "content": task},
                     {"role": "user", "content": "the following message contains input.csv content, please print sorted by timestamp content for output.csv"},
                     {"role": "user", "content": file_content}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=talk_messages,
    )
    talk_response = response["choices"][0]["message"]
    print(talk_response["content"])
    talk_messages.append(talk_response)


run_conversation()
