import openai
import json


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = 'Create a file organizer CLI tool in Python that sorts files in a ' + \
           'directory based on their file types (e.g., images, documents, ' + \
           'audio) and moves them into these corresponding folders: ' + \
           "'images', 'documents', 'audio'. The entry point will be a python " + \
           'file that can be run this way: python organize_files.py ' + \
           '--directory_path=YOUR_DIRECTORY_PATH'

    print(task)

    messages = [{"role": "system", "content": "You are heplfull assistant"},
                {"role": "user",
                 "content": "Please tell which function of 'read_file' or 'write_file' would solve following task, answer only 'read_file' or 'write_file':"
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
    response_message = response["choices"][0]["message"]
    print(response_message)

run_conversation()