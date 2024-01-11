from user_input_getter import UserInputHandler


def get_user_request(user_input_handler):
    user_input = input('''Select input type:
1) Text
2) Speech
''')

    if user_input == "1":
        return user_input_handler.recognize_from_text()
    elif user_input == "2":
        return user_input_handler.recognize_from_microphone()
    else:
        print("Error Input")


if __name__ == "__main__":
    user_input_handler = UserInputHandler('test-deployment')
    output_data = get_user_request(user_input_handler)
    if output_data:
        print("DISH: " + output_data['dish_name'])
        print("SERVING COUNT: " + str(output_data['serving_count']))