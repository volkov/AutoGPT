import openai
import json
import asyncio
from forge.agent import ForgeAgent


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = ("Sort the input.csv by the 'timestamp' column and write the new csv in the output.csv file. "
            "The order of the columns should be preserved.")
    file_content = ("id,name,timestamp\n"
                    "3,Alice,2023-09-25 14:10:00\n"
                    "1,Bob,2023-09-24 12:05:00\n"
                    "2,Charlie,2023-09-24 12:10:00\n"
                    "4,David,2023-09-26 16:20:00\n")
    print("#####")
    print("Task:")
    print(task)
    print("#####")
    print("File content:")
    print(file_content)

    model = "gpt-3.5-turbo-0613"
    #model = "gpt-4-0613"

    print()
    print()
    print('############')
    print("Model talks w agent:")

    agent = ForgeAgent(None, None)
    messages = asyncio.run(agent.format_messages_for_task("talk", task))
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    talk_response = response["choices"][0]["message"]
    print(talk_response["content"])


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
