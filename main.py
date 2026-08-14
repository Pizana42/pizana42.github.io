import random
from pyscript import web, when # type: ignore

s = {
    "scores": [],
    "highscore": None,
    "num": None,
    "tries": 0,
    "out": ""
}

def start_game():
    s["scores"] = []
    s["highscore"] = None
    s["num"] = None
    s["tries"] = 0
    s["out"] = ""
    web.page["output"].innerText = ""
    new_round()

def new_round():
    s["num"] = random.randint(1,100)
    s["tries"] = 0

def handle_input(command):
    if command in ("q", "quit", "exit"):
        s["out"] += "\n" + f"Dein Highscore war: {s['highscore']}"
        s["out"] += "\n" + f"Deine Scores waren: {', '.join(s['scores'])}"
        exit()
    elif command in ("s", "score", "highscore"):
        s["out"] += "\n" + f"Dein aktueller Highscore ist: {s['highscore']}"
        s["out"] += "\n" + f"Deine bisherigen Scores sind: {', '.join(s['scores'])}"
    elif command in ("h", "hilfe", "help"):
        s["out"] += "\n" + "Verfügbare Abkürzungen:\n  q  =  \"quit\"\n  s  =  \"score\"\n  h  =  \"hilfe\"\n  r  =  reset\n  c  =  \"cheat\"\nWarte was, es gibt cheats?"
    elif command in ("c", "cheat"):
        s["out"] += "\n" + "Pssst... Willst du ne Acht kaufen?"
        s["num"] = 8
    elif command in ("r", "reset", "clear"):
        start_game()
    else:
        try:
            return int(command)
        except ValueError:
            s["out"] += "\n" + "Keine gültige Eingabe!"

def check_guess(guess):
    if guess > s["num"]:
        s["out"] += "\n" + f"Meine Zahl ist kleiner als {guess}"
    elif guess < s["num"]:
        s["out"] += "\n" + f"Meine Zahl ist größer als {guess}"
    else:
        s["out"] += "\n" + f"Bravo! Du hast die Zahl erraten! Du hast {s['tries']} Versuche gebraucht."
        s["scores"].append(str(s["tries"]))
        if s["highscore"] == None:
            s["out"] += "\n" + f"{s['tries']} ist dein erster Highscore. Kannst du ihn verbessern?"
            s["highscore"] = s["tries"]
        elif s["highscore"] > s["tries"]:
            s["out"] += "\n" + f"Damit hast du deinen alten Highscore von {s['highscore']} übertroffen!"
            s["highscore"] = s["tries"]
        else:
            s["out"] += "\n" + f"Dein Highscore bleibt weiterhin {s['highscore']}"
        new_round()

def send_output():
    s["out"] = "\n---" + s["out"]
    output = web.page["output"]
    output.innerText = s["out"] + output.innerText
    web.page["input"].value = ""
    s["out"] = ""



start_game()

@when("click", "button")
def send_guess():
    command = web.page["input"].value
    if not command:
        return

    guess = handle_input(command)
    if guess is not None:
        s["tries"] += 1
        check_guess(guess)

    send_output()

@when("keypress", "input")
def enter_guess(event):
    if event.key == "Enter":
        send_guess()