from google import genai
model_name = "gemini-2.0-flash"
api_key = "AIzaSyD5Rrr8LtlnQfJSOq3NS4TTIGJW6FmwUbM"

client = genai.Client(api_key=api_key)
# chat = client.chats.create(model=model_name)

# # uploaded_file = client.files.upload(file="image.png")
# # response = chat.send_message(["私の名前はROROというロボットです．こんな見た目をしています．", uploaded_file])
# uploaded_file = client.files.upload(file="sound.wav")
# response = chat.send_message(["これは何の音でしょうか？ヒントは乗り物の音です！", uploaded_file])
# print(response.text)
# print("===============================================")
# # response = chat.send_message("私の目は何でできてるでしょうかーーー？？")
# # response = chat.send_message("違います！ヒントは乗り物の音です！")
# response = chat.send_message("他の音当てクイズしたいです！なにか出して！")
# print(response.text)
# print(response)


# print("\033[32m\n\n===============================================\n\n\033[0m")

# for message in chat.get_history():
#     print(f'role - {message.role}',end=": ")
#     print(message.parts[0].text)

contents_list = []
# contents_list = [{"role": "user", "parts": [{"text": """You are an AI robot.
# Select from the function_list the next function to be performed based on the instructions sent and past transitions.
# The response should return only one "Function(arg)" selected from the function_list.

# function_list
# - Navigation(arg)
#   - Function to move to arg.
#   - arg is selected from location_list.
#   - The result is “SUCCESS” or “FAILED”.
# - GraspObject(arg)
#   - A function that grasps arg.
#   - The arg is selected from the object_list.
#   - The result is “SUCCESS” or “FAILED”.
# - PlaceObject()
#   - Function to place the object you are holding on a table or desk.
#   - No arg.
#   - This function is performed after Navigation() to the table or desk where you want to place it.
#   - The result is “SUCCESS” or “FAILED”.
# - PassObject()
#   - Function to pass the object you have to the person.
#   - No arg.
#   - This function is performed after Navigation() to the table or desk where you want to place it.
#   - The result is “SUCCESS” or “FAILED”.
# - FindObject()
#   - Function to search for objects in front of the robot.
#   - No arg.
#   - If there are multiple objects in front of the robot, [A,B,C,C,C] is returned in duplicate.
#   - If there is no object to find, navigation to the next position is performed.
#   - The result is a “list of objects” found in object_list.
# - End()
#   - Function to be called when all the contents of the imperative statement have been completed.
#   - No arg.
#   - This resets the instruction.

# location_list
# - instruction_point
# - kitchen#table
# - kitchen#chair
# - kitchen#trash_box
# - living_room#table
# - living_room#sofa

# object_list
# - lunch_box
# - snack
# - detergent
# - cup
# - noodle
# - apple

# Additional Information
# - Your name is SOBIT HOME
# - You are a robot with one arm
# - My name is Axel
# - Now, Axel and SOBIT HOME are at instruction_point
# - Today is May 5.
# - It is now 12:00.

# The input should be in the following form:
# “
# Imperative Statement : imperative statement
# Past Transitions :
# - Function1(arg) -> Result
# - Function2(arg) -> Result
# - Function3(arg) -> Result
# - ・・・
# - Functionn(arg) -> Result
# “

# The reply should be in the following form:
# “
# Function(arg)
# “

# Are you ready?
# """}]}, {"role": "model", "parts": [{"text": "I am ready."}]}]
# uploaded_file = client.files.upload(file="image.png")
# uploaded_file = client.files.upload(file="sound.wav")
# uploaded_file = client.files.upload(file="audio.mp3")
uploaded_file1 = client.files.upload(file="image.png")
uploaded_file2 = client.files.upload(file="test.jpg")
contents_list += [{"role": "user",
                "parts": [
                        {"text": "2つの画像からなにかお話しませんか？？"},
                        {"file_data":
                            {"mime_type": uploaded_file2.mime_type,
                            "file_uri": uploaded_file2.uri}
                        },
                        {"file_data":
                            {"mime_type": uploaded_file1.mime_type,
                            "file_uri": uploaded_file1.uri}
                        },
                    ]
                }]

result = ""
for chunk in client.models.generate_content_stream(   ## generate_content
    model=model_name,
    contents=contents_list,
):
    print(chunk.text, end="")
    result += chunk.text
contents_list += [{"role": "model", "parts": [{"text": str(result)}]}]
print()
# contents_list += [{"role": "model", "parts": [{"text": "ロボットですね！"}]}]

# uploaded_file = client.files.upload(file="sound.wav")
# contents_list += [{"role": "user",
#                 "parts": [
#                         {"text": "そうです！動くときにこんな音が鳴ります！何の音に似てますか？"},
#                         {"file_data":
#                             {"mime_type": uploaded_file.mime_type,
#                             "file_uri": uploaded_file.uri}
#                         }
#                     ]
#                 }]

# contents_list += [{"role": "model", "parts": [{"text": "雷の音に聞こえますね・・・！"}]}]

# while True:
for i in range(4):
    input_text = ""
    input_text = str(input("USER : "))
    # if (i==0):
    #     uploaded_file = client.files.upload(file="image.png")
    #     contents_list += [{"role": "user",
    #                     "parts": [
    #                             {"text": input_text},
    #                             {"file_data":
    #                                 {"mime_type": uploaded_file.mime_type,
    #                                 "file_uri": uploaded_file.uri}
    #                             }
    #                         ]
    #                     }]
    # if (i==1):
    #     uploaded_file = client.files.upload(file="sound.wav")
    #     contents_list += [{"role": "user",
    #                     "parts": [
    #                             {"text": input_text},
    #                             {"file_data":
    #                                 {"mime_type": uploaded_file.mime_type,
    #                                 "file_uri": uploaded_file.uri}
    #                             }
    #                         ]
    #                     }]
    # else:
    #     contents_list += [{"role": "user",
    #                     "parts": [
    #                             {"text": input_text}
    #                         ]
    #                     }]
    contents_list += [{"role": "user",
                    "parts": [
                            {"text": input_text}
                        ]
                    }]

    # result = client.models.generate_content(   ## generate_content_stream
    #     model=model_name,
    #     contents=contents_list,
    # )
    # contents_list += [{"role": "model", "parts": [{"text": str(result.text)}]}]

    # print(result.text)

    result = ""
    for chunk in client.models.generate_content_stream(   ## generate_content
        model=model_name,
        contents=contents_list,
    ):
        print(chunk.text, end="")
        result += chunk.text
    contents_list += [{"role": "model", "parts": [{"text": str(result)}]}]
    print()
    # print("\033[31m===============================")
    # print(contents_list)
    # print("===============================\033[0m")
