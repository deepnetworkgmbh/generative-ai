from user_input_getter import recognize_from_microphone
from user_input_getter import recognize_from_text


def get_user_request():
    user_input = input('''Select input type:
1) Text
2) Speech
''')

    if user_input == "1":
        return recognize_from_text()
    elif user_input == "2":
        return recognize_from_microphone()
    else:
        print("Error Input")


output_data = get_user_request()
if output_data:
    print("DISH: " + output_data['dish_name'])
    print("SERVING COUNT: " + str(output_data['serving_count']))
