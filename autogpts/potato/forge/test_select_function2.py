import openai
import json


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = 'Read the file called file_to_read.txt and write its content to a file called output.txt'
    print(task)

    messages = [{"role": "system", "content": "You are heplfull assistant, Please tell which function of 'read_file' or 'write_file' would solve following task, answer only 'read_file' or 'write_file':"},
                {"role": "user",
                 "content": ""
                            "\n##Task\n" + task}]
    functions = [
        {'description': 'Read data from a file',
         'name': 'read_file',
         'parameters': {'properties': {'file_path': {'description': 'Path to the file',
                                                     'type': 'string'}},
                        'type': 'object'}},
        {'description': 'Write data to a file',
         'name': 'write_file',
         'parameters': {'properties': {'data': {'description': 'Data to write to the '
                                                               'file',
                                                'type': 'string'},
                                       'file_path': {'description': 'Path to the file',
                                                     'type': 'string'}},
                        'type': 'object'}}]
    # model = "gpt-4-0613"
    model = "gpt-3.5-turbo-0613"
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # functions=functions,
        # function_call={"name": "write_file"},  # auto is default, but we'll be explicit
    )
    print(response["choices"][0]["message"])

    messages = [{"role": "system", "content": "You are heplfull assistant, Please call function which solve following task"},
                {"role": "user",
                 "content": ""
                            "\n##Task\n" + task}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call={"name": "read_file"},  # auto is default, but we'll be explicit
    )
    print(response["choices"][0]["message"])
run_conversation()