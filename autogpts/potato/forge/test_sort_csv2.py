import openai
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

    messages = [{'content': 'You are heplfull assistant.', 'role': 'system'},
     {'content': "Sort the input.csv by the 'timestamp' column and write the new "
                 'csv in the output.csv file. The order of the columns should be '
                 'preserved.\n'
                 'Your previous action was to run function {"name": "read_file", '
                 '"arguments": "{\\n  \\"file_path\\": \\"input.csv\\"\\n}"}\n'
                 "It's output was:\n"
                 'id,name,timestamp\n'
                 '3,Alice,2023-09-25 14:10:00\n'
                 '1,Bob,2023-09-24 12:05:00\n'
                 '2,Charlie,2023-09-24 12:10:00\n'
                 '4,David,2023-09-26 16:20:00\n',
      'role': 'user'},
     {
         "role": "assistant",
         "content": "To sort the input.csv by the 'timestamp' column and write the new csv in the output.csv file, you can use the following code:\n\n```python\nimport pandas as pd\n\n# Read the input.csv file\ndf = pd.read_csv('input.csv')\n\n# Sort the dataframe by the 'timestamp' column\ndf_sorted = df.sort_values('timestamp')\n\n# Write the sorted dataframe to the output.csv file\ndf_sorted.to_csv('output.csv', index=False)\n```\n\nThis code uses the pandas library to read the input.csv file into a dataframe, sorts the dataframe by the 'timestamp' column, and then writes the sorted dataframe to the output.csv file. The `index=False` parameter is used to exclude the index column from the output file."
     },
     {'content': 'Please call function which solve task.\n'
                 'Ensure that arguments are correct.',
      'role': 'system'},
     {'content': '', 'role': 'user'}]
    print('############')
    print("Model runs function:")
    agent = ForgeAgent(None, None)
    functions = agent.abilities.list_abilities_functions()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call={"name": "write_file"},
    )
    function_call = response["choices"][0]["message"].get("function_call")
    asyncio.run(agent.run_ability("test", function_call))



run_conversation()
