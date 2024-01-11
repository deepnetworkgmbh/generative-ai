from user_input_handler import UserInputHandler


class UserInputGetter():

    def __init__(self, azure_openai_model):
        self.azure_openai_model = azure_openai_model

    def get_user_request(self):
        user_input_handler = UserInputHandler(self.azure_openai_model)
        user_input = input("Select input type: \n 1) Text \n 2) Speech \n")

        if user_input == "1":
            output_data = user_input_handler.recognize_from_text()
        elif user_input == "2":
            output_data = user_input_handler.recognize_from_microphone()
        else:
            print("Error Input")

        if output_data:
            return output_data['dish_name'], output_data['serving_count']
        else:
            return None, None
