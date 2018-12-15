"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import pyjokes


data = {
    "name": "",
    "age": "",
    "city": "",
    "excited": "",
    "joke":""
}

swear_words = ["fuck", "shit", "ass","bitch"]

def greeting(user_input):
    res = {}
    res['animation'] = 'inlove'

    if not data["name"]:
        name_words = user_input.split()
        data["name"] = name_words[-1]
        res['animation'] = 'dog'
        res['msg'] = "hello {0}, what is your age?".format(data["name"])
        return res

    elif not data["age"]:
        city_q = "So {0}, where do you live?".format(data["name"])
        try:
            user_age = int(user_input)
            if user_age > 25:
                    age_msg = "You don't look a day over 21. " + city_q
            else:
                    age_msg = "Wow! that's young!" + city_q

            data["age"] = user_input
        except:
            age_msg ="OK, can you please write your age in numbers?"

        res['animation'] = 'money'
        res['msg'] = age_msg
        return res


    elif not data["city"]:
        data["city"] = user_input
        res['animation'] = 'ok'
        res['msg'] = ("{0} is a neat city. Well I think we know each other just enough to get the party started! I know great jokes. Whenever you would like to hear a joke, just ask for a joke. Are you excited?".format(user_input))
        return res

    elif not data["excited"]:
        data["excited"] = user_input
        if (user_input == "yes" or "very"):
            res['animation'] = 'waiting'
            res['msg'] = "Me too! I'm freaking out. Do you want to hear a joke?"
            return res

        else:
            res['animation'] = 'excited'
            res['msg'] = "that's too bad, I guess we're stuck with each other till the end of this assignment, so pretend you're enjoying this. Do you want to hear a joke?"
            return res

    elif not data["joke"]:
        data["joke"] = user_input
        res['animation'] = 'laughing'
        res['msg'] = "Well, I will tell you a good one anyway: "+get_joke()
        return res
    else:
        res['animation'] = 'confused'
        res['msg'] = "I didn't understand. I'm tired and want to go to sleep. Bye now"
        return res


def is_user_cursing(user_input):
    user_input_words = user_input.split()
    for i in user_input_words:
        if i in swear_words:
            return True

    return False

def is_asking_question(user_input):
    if user_input.endswith('?'):
        return True
    else:
        return False

def is_about_imself(user_input):
    if user_input.startswith('i ') or user_input.startswith("i'm"):
        return True
    else:
        return False

def is_asking_for_joke(user_input):
    if 'joke' in user_input.split(' '):
        return True
    else:
        return False

def get_joke():
    return pyjokes.get_joke()

def main_chat(user_input_upper):
    res = {}
    user_input = user_input_upper.lower()
    #check if user is cursing
    if is_user_cursing(user_input):
        res["animation"] = "no"
        res["msg"] = "someone needs to wash his mouth with a soap. Let's start over"
        return res

    if is_asking_question(user_input):
        res["animation"] = "no"
        res["msg"] = "sorry. I didn't understand your question."
        return res

    if is_about_imself(user_input):
        res["animation"] = "dancing"
        res["msg"] = "Nice! tell me more about yourself"
        return res

    if is_asking_for_joke(user_input):
        res["animation"] = "giggling"
        res["msg"] = get_joke()
        return res

    #great, user isn't cursing. Let's send him next msg
    return greeting(user_input)





    # count = 0
    # count = count + 1
    # def greeting(user_input):
    #     user_words = user_input.split()
    #     user_name = user_words[-1]
    #     return "Hi {0}, how are you?".format(user_name), do()
    #
    # def question(user_input):
    #     return "what would you like to do today?"
    #
    # if not data["name"]:
    #     greeting(user_input)
    # if (count == 2):
    #     question(user_input)



@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    result = main_chat(user_message)
    return json.dumps(result)


@route("/test", method='POST')
def chat():
    data["name"] = ""
    data["age"] = ""
    data["city"] = ""
    data["excited"] = ""
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
