from user_input_getter import recognize_from_microphone
from user_input_getter import recognize_from_text

# user_input = input('''Select input type:
# 1) Text
# 2) Speech
# ''')

user_input = "1"
if user_input == "1":
    recognize_from_text()
elif user_input == "2":
    recognize_from_microphone()
else:
    print("Error Input")
