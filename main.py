import telebot
import json
import os

with open("token.txt", "r") as token_file:
    bot = telebot.TeleBot(token_file.read())


@bot.message_handler(commands=["start"])
def starting_handler(message):
    bot.send_message(message.from_user.id, f"Hello and welcome to the To-Do manager bot!\nUse /help for a list of commands.")


@bot.message_handler(commands=["help"])
def help_handler(message):
    with open("help_message_text.txt", "r") as f:
        text = f.read()
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=["new_task"])
def start_creating_new_task(message):
    msg = bot.send_message(message.from_user.id, "What task do you want to add?")
    bot.register_next_step_handler(msg, create_new_task)


def create_new_task(message):
    if message.text.lower() == "quit":
        bot.send_message(message.from_user.id, "Quitting.")
    else:
        if os.path.isfile(f"lists/{message.from_user.id}.json"):
            with open(f"lists/{message.from_user.id}.json", "r") as f:
                json_dict = json.loads(f.read())
                json_dict["active_tasks"].append(f"{message.text}")
            with open(f"lists/{message.from_user.id}.json", "w") as f:
                f.write(json.dumps(json_dict))
        else:
            with open(f"lists/{message.from_user.id}.json", "w") as f:
                json_dict = {"active_tasks": [f"{message.text}"]}
                f.write(json.dumps(json_dict))
        bot.send_message(message.from_user.id, "Created new task for you!")


@bot.message_handler(commands=["set_done"])
def start_setting_as_done(message):
    if os.path.isfile(f"lists/{message.from_user.id}.json"):
        msg = bot.send_message(message.from_user.id, "What task do you want to set as done?")
        bot.register_next_step_handler(msg, set_as_done)
    else:
        bot.send_message(message.from_user.id, "You don`t have any active tasks!")


def set_as_done(message):
    if message.text.lower() == "quit":
        bot.send_message(message.from_user.id, "Quitting.")
    else:
        with open(f"lists/{message.from_user.id}.json", "r") as f:
            json_dict = json.loads(f.read())
            del json_dict["active_tasks"][json_dict["active_tasks"].index(f"{message.text}")]
        with open(f"lists/{message.from_user.id}.json", "w") as f:
            f.write(json.dumps(json_dict))
        bot.send_message(message.from_user.id, "Set the task as done!")


@bot.message_handler(commands=["tasks_list"])
def tasks_list_command(message):
    if os.path.isfile(f"lists/{message.from_user.id}.json"):
        with open(f"lists/{message.from_user.id}.json", "r") as f:
            tasks_list = json.loads(f.read())["active_tasks"]
            text = "Currently active tasks:\n"
            for task in tasks_list:
                text += f"- {task}\n"
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "You don`t have any active tasks!")


def main():
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
