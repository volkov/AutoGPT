import openai
import json


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    task2 = 'Create a file organizer CLI tool in Python that sorts files in a ' + \
            'directory based on their file types (e.g., images, documents, ' + \
            'audio) and moves them into these corresponding folders: ' + \
            "'images', 'documents', 'audio'. The entry point will be a python " + \
            'file that can be run this way: python organize_files.py ' + \
            '--directory_path=YOUR_DIRECTORY_PATH'

    task = 'Create a random password generator. The password should have ' + \
           'between 8 and 16 characters and should contain letters, numbers ' + \
           'and symbols. The password should be printed to the console. The ' + \
           'entry point will be a python file that can be run this way: ' + \
           'python password_generator.py [--len x] where x is the length of ' + \
           'the password. If no length is specified, the password should be ' + \
           '8 characters long. The password_generator can also be imported ' + \
           'as a module and called as password = ' + \
           'password_generator.generate_password(len=x). Any invalid input ' + \
           'should raise a ValueError.'
    print(task2)
    messages = [{"role": "system", "content": "You are heplfull assistant"},
                {"role": "user", "content": task2 }]
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
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(response_message)

    # Step 2: check if GPT wanted to call a function
    call = response_message.get("function_call")
    if call:
        # print(call)
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


print(run_conversation())
