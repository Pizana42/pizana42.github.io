import random
from pyscript import web, when # type: ignore

difficulty = 100

s = {
    "scores": [],
    "highscore": None,
    "num": None,
    "tries": 0,
    "out": "",
    "theme": "dark"
}

def reset_game():
    s["highscore"] = None
    s["scores"] = []
    s["out"] = ""
    web.page["output"].innerText = ""
    new_round()

def new_round():
    s["num"] = random.randint(1,difficulty)
    s["tries"] = 0

def handle_input(command):
    if command in (".1", ".", "h", "hilfe", "help"):
        s["out"] += "\n" + "Verfügbare Abkürzungen:\n.1 = hilfe\n.2 = score\n.3 = reset \n.4 = cheat\nWarte was, es gibt cheats?"
    elif command in (".2", ",", "s", "score", "highscore"):
        s["out"] += "\n" + f"Dein aktueller Highscore ist: {s['highscore']}"
        s["out"] += "\n" + f"Deine bisherigen Scores sind: {', '.join(str(score) for score in s['scores'])}"
    elif command in (".3", "r", "reset", "clear"):
        reset_game()
    elif command in (".4", "-", "c", "cheat"):
        s["out"] += "\n" + "Pssst... Willst du ne Acht kaufen?"
        s["tries"] = difficulty + 1
        s["num"] = 8
    else:
        try:
            return int(command)
        except ValueError:
            s["out"] += "\n" + "Keine gültige Eingabe!"

def check_guess(guess):
    if guess > s["num"]:
        s["out"] += "\n" + f"Meine Zahl ist kleiner als {guess}."
    elif guess < s["num"]:
        s["out"] += "\n" + f"Meine Zahl ist größer als {guess}."
    else:
        if s["tries"] > difficulty:
            s["out"] += "\n" + f"Du hast die Zahl erraten. Aber auf eine eher traurige Art und Weise."
            s["out"] += "\n" + f"Diese Runde wird auf jeden Fall nicht als Highscore in die Geschichte eingehen!"
        elif s["tries"] == 1:
            s["out"] += "\n" + f"Wie bitte? Du hast die Zahl {s['num']} in nur einem Versuch erraten? Mentalist!"
            apply_score()
        else:
            s["out"] += "\n" + f"Bravo! Du hast die Zahl {s['num']} erraten und {s['tries']} Versuche gebraucht!"
            apply_score()
        new_round()
    if guess > difficulty or guess < 1:
        s["out"] += "\n" + "Aber das zählen wir mal nicht..."
        s["tries"] -= 1

def apply_score():
    if s["highscore"] == None:
        s["out"] += "\n" + f"{s['tries']} ist dein erster Highscore. Kannst du ihn verbessern?"
    elif s["highscore"] > s["tries"]:
        s["out"] += "\n" + f"Damit hast du deinen alten Highscore von {s['highscore']} verbessert!"
    else:
        s["out"] += "\n" + f"Dein Highscore bleibt weiterhin {s['highscore']}."
    s["scores"].append(s["tries"])
    s["highscore"] = min(s["scores"])

def send_output():
    s["out"] = "\n---" + s["out"]
    output = web.page["output"]
    output.innerText = s["out"] + output.innerText
    web.page["input"].value = ""
    s["out"] = ""



reset_game()

@when("click", "#submit")
def send_guess():
    command = web.page["input"].value.lower()
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

@when("click", "#theme")
def switch_theme():
    style = web.page.html.style
    if s["theme"] == "light":
        style["background-color"] = "#181a1b"
        style["--input-bg-color"] = "#232627"
        style["color"] = "#e8e6e3"
        s["theme"] = "dark"
    else:
        style["background-color"] = "#ffffff"
        style["--input-bg-color"] = "#ffffff"
        style["color"] = "#000000"
        s["theme"] = "light"