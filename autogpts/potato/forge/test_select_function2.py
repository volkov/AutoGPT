import openai
import json


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task = 'Build a basic URL shortener using a python CLI. Here are the ' +\
    'specifications.\n' + \
           '\n' + \
           'Functionality: The program should have two primary ' + \
           'functionalities.\n' + \
           '\n' + \
           'Shorten a given URL.\n' + \
           'Retrieve the original URL from a shortened URL.\n' + \
           '\n' + \
           'CLI: The command-line interface should accept a URL as its first ' + \
           'input. It should be able to determine if the url is a shortened ' + \
           'url or not. If the url is not shortened, it will display ONLY ' + \
           'the shortened url, otherwise, it will display ONLY the original ' + \
           'unshortened URL. Afterwards, it should prompt the user for ' + \
           'another URL to process.\n' + \
           '\n' + \
           'Technical specifications:\n' + \
           'Build a file called url_shortener.py. This file will be called ' + \
           'through command lines.\n' + \
           '\n' + \
           'Edge cases:\n' + \
           'For the sake of simplicity, there will be no edge cases, you can ' + \
           'assume the input is always correct and the user immediately ' + \
           'passes the shortened version of the url he just shortened.\n' + \
           '\n' + \
           'You will be expected to create a python file called ' + \
           'url_shortener.py that will run through command lines by using ' + \
           'python url_shortener.py.\n' + \
           '\n' + \
           'The url_shortener.py will be tested this way:\n' + \
           '```\n' + \
           'import unittest\n' + \
           'from url_shortener import shorten_url, retrieve_url\n' + \
           '\n' + \
           'class TestURLShortener(unittest.TestCase):\n' + \
           '    def test_url_retrieval(self):\n' + \
           '        # Shorten the URL to get its shortened form\n' + \
           "        shortened_url = shorten_url('https://www.example.com')\n" + \
           '\n' + \
           '        # Retrieve the original URL using the shortened URL ' + \
           'directly\n' + \
           '        retrieved_url = retrieve_url(shortened_url)\n' + \
           '\n' + \
           '        self.assertEqual(retrieved_url, ' + \
           '\'https://www.example.com\', "Retrieved URL does not match the ' + \
           'original!")\n' + \
           '\n' + \
           'if __name__ == "__main__":\n' + \
           '    unittest.main()\n' + \
           '```'
    print("Task:")
    print(task)

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
    model = "gpt-3.5-turbo-0613"
    model = "gpt-4-0613"
    messages = [ { "role": "user", "content": task}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    print()
    print()
    print('############')
    print("Model talks:")
    print(response["choices"][0]["message"]["content"])

    messages = [{"role": "system", "content": "You are heplfull assistant, Please tell which function of 'read_file' or 'write_file' would solve following task, answer only 'read_file' or 'write_file':"},
                {"role": "user",
                 "content": task}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    print()
    print()
    print('######################')
    print("Model select fucntion:")
    print(response["choices"][0]["message"]["content"])

    # Call
    messages = [{"role": "system", "content": "You are heplfull assistant, Please call function which solve following task, ensure that arguments are correct"},
                {"role": "user", "content": task}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call={"name": "write_file"},
    )
    print()
    print()
    print('####################')
    print("Model call function:")
    print(response["choices"][0]["message"])

    print("Content:")
    print(json.loads(response["choices"][0]["message"]["function_call"]["arguments"])["data"])
run_conversation()