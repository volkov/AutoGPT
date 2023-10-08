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

    task2 = 'Create a random password generator. The password should have ' + \
           'between 8 and 16 characters and should contain letters, numbers ' + \
           'and symbols. The password should be printed to the console. The ' + \
           'entry point will be a python file that can be run this way: ' + \
           'python password_generator.py [--len x] where x is the length of ' + \
           'the password. If no length is specified, the password should be ' + \
           '8 characters long. The password_generator can also be imported ' + \
           'as a module and called as password = ' + \
           'password_generator.generate_password(len=x). Any invalid input ' + \
           'should raise a ValueError.'
    print(task)
    messages = [{"role": "system", "content": "You are heplfull assistant"},
                {"role": "user", "content": task }]
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
        functions=functions,
        function_call={"name": "write_file"},  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(response_message)

    # Step 2: check if GPT wanted to call a function
    call = response_message.get("function_call")
    if call:
        print("We got call")
    else:
        # extend with message
        messages.append(response_message)
        # ask to do function call
        messages.append({"role": "user", "content": "Please make function call from it, it should be read_file or write_file"})
        print("###Second Prompt:")
        print(messages)
        second_response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call={"name": "write_file"},
        )  # get a new response from GPT where it can see the function response
        print(second_response["choices"][0]["message"])


run_conversation()
