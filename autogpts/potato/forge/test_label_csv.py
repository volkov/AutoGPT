import openai
import asyncio
from forge.agent import ForgeAgent


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = ("The csv 'input.csv' has many items. "
            "create a 'Color' column for these items and classify them "
            "as either 'blue', 'green', or 'yellow' depending on what the most likely color is. "
            "Preserve the order of the rows. The color column should be the second column. "
            "Write the output in output.csv")
    file_content = ("Item\n"
                    "Banana\n"
                    "Leaf\n"
                    "Sky\n"
                    "Sunflower\n"
                    "Grass\n"
                    "Jeans\n"
                    "Lemon\n"
                    "Tree\n"
                    "Ocean\n"
                    "Daisy\n"
                    "Fern\n")
    print("#####")
    print("Task:")
    print(task)
    print("#####")
    print("File content:")
    print(file_content)

    #model = "gpt-3.5-turbo-0613"
    model = "gpt-4-0613"

    print('############')
    print("Model select function:")
    agent = ForgeAgent(None, None)
    messages = asyncio.run(agent.format_messages_for_task("select", task))
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        #functions=functions,
        #function_call={"name": "write_file"},
    )
    print(response["choices"][0]["message"])
    #asyncio.run(agent.run_ability("test", function_call))



run_conversation()
