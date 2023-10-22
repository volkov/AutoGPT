import openai
import asyncio
from forge.agent import ForgeAgent


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = ("The csvs 'file1.csv' and 'file2.csv' both have a column 'ID'. "
            "Combine these 2 csvs using the 'ID' column. "
            "Sort the rows by ID in ascending order and the columns alphabetically. "
            "Write the output in output.csv")

    task_w_data = ("The csvs 'file1.csv' and 'file2.csv' both have a column 'ID'. "
                   "Combine these 2 csvs using the 'ID' column. Sort the rows by ID "
                   'in ascending order and the columns alphabetically. Write the '
                   'output in output.csv\n'
                   'Your previous action was to run function {"name": "read_file", '
                   '"arguments": "{\\n  \\"file_path\\": \\"file1.csv\\"\\n}"}\n'
                   "It's output was:\n"
                   'ID,Name,Age\n'
                   '101,John,28\n'
                   '102,Alice,34\n'
                   '103,Bob,45\n'
                   '\n'
                   'Your previous action was to run function {"name": "read_file", '
                   '"arguments": "{\\n  \\"file_path\\": \\"file2.csv\\"\\n}"}\n'
                   "It's output was:\n"
                   'ID,Occupation,Salary\n'
                   '101,Engineer,80000\n'
                   '102,Doctor,120000\n'
                   '103,Lawyer,95000\n')

    file_content = ("ID,Age,Name,Occupation,Salary\n"
                    "101,28,John,Engineer,80000\n"
                    "102,34,Alice,Doctor,120000\n"
                    "103,45,Bob,Lawyer,95000\n")
    print("#####")
    print("Task:")
    print(task)
    print("#####")
    print("File content:")
    print(file_content)

    model = "gpt-3.5-turbo-0613"
    #model = "gpt-4-0613"

    messages = [
        {'content': 'Review following output and task', 'role': 'system'},
        {'content': "Task is:\n" + task_w_data, 'role': 'user'},
        {'content': "Content of output.csv:\n" + file_content, 'role': 'user'},
        {'content': 'First work out your own file content. Then compare your file with provided', 'role': 'user'}
    ]
    print('############')
    print("Model rethink:")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    print(response["choices"][0]["message"]["content"])



run_conversation()
