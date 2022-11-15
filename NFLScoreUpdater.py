from bs4 import BeautifulSoup
import requests
import re
import time
import random

url = "http://www.thescore.com/nfl/events"

def main():
    games_raw = get_game_data(url)

    print(f"{len(games_raw)} games this week")

    games = clean_data(games_raw)

    for game in games:
        #game["status"] = "End 4th"
        print(print_game(game))
        print("-----------------------")
    print("-----------------------")
    
    while True:
        wait_time = random.randint(60, 120)
        time.sleep(wait_time)
        
        games_raw = get_game_data(url)
        
        updated_games = clean_data(games_raw)
        
        for i in range(len(games)):
            game = games[i]
            for j in range(len(updated_games)):
                updated_game = updated_games[j]
                if game["team0"] == updated_game["team0"]:
                    break
            
            # Find any updates and print the alert and scores
            alert = compare_games(game, updated_game)
            if alert:
                print(alert)
                print(print_game(updated_game))
                print("-----------------------")
            elif "M" in game["status"] and "M" not in updated_game["status"]:# Start of a game
                print(print_game(updated_game))
                print("-----------------------")
            elif "End" not in game["status"] and "End" in updated_game["status"]:# End of a qtr
                print(print_game(updated_game))
                print("-----------------------")
            elif "Halftime" not in game["status"] and "Halftime" in updated_game["status"]:# Halftime
                print(print_game(updated_game))
                print("-----------------------")
            elif "Final" not in game["status"] and "Final" in updated_game["status"]:# End of a game
                print(print_game(updated_game))
                print("-----------------------")
        
        print("-----------------------")
        games = updated_games
        
        
        
def get_game_data(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc.find_all("div", {"class": "col-xs-12 col-md-6"})


def clean_data(games_raw):
    games = []
    for game_raw in games_raw:
        gamestr = str(game_raw)
        #print(gamestr)
        
        teams = re.findall(r">([A-Z]{2,3} [A-Za-z0-9]+)</div>", gamestr)
        scores = re.findall(r"EventCard__score-.*>([0-9]{1,2})</div>", gamestr)

        timestart = re.search(r"clockColumn--.*>([0-9]{1,2}:[0-9]{2} [A-Z]M)</div>", gamestr)
        if timestart:
            scores = ["0", "0", timestart.group(1)]

        clock = re.search(r"clockColumn--.*>([0-9]{1,2}:[0-9]{2} [1-4][a-z]{2})</div>", gamestr)
        if clock:
            scores.append(clock.group(1))
        
        ot_clock = re.search(r"clockColumn--.*>([0-9]{1,2}:[0-9]{2} OT)</div>", gamestr)
        if ot_clock:
            scores.append(ot_clock.group(1))

        endqtr = re.search(r"clockColumn--.*>(End [1-4][a-z]{2})</div>", gamestr)
        if endqtr:
            scores.append(endqtr.group(1))

        if (halftime := re.search(r"Halftime", gamestr)):
            scores.append("Halftime")

        if (final := re.search(r"Final .OT.", gamestr)):
            scores.append("Final (OT)")
        elif (final := re.search(r"Final", gamestr)):
            scores.append("Final")
        
        #print(teams)
        #print(scores)

        games.append({"team0":teams[0], "team1":teams[1], "score0":scores[0], "score1":scores[1], "status":scores[2]})
    
    return games


def compare_games(game, updated_game):
    for i in range(2):
        if game[f"score{i}"] != updated_game[f"score{i}"]:
            score_difference = int(updated_game[f"score{i}"]) - int(game[f"score{i}"])
            if score_difference == 1:
                alert = f"{game[f'team{i}']} scored an extra point!"
            elif score_difference == 2:
                alert = f"{game[f'team{i}']} scored a safety or 2-pt converstion!"
            elif score_difference == 3:
                alert = f"{game[f'team{i}']} scored a field goal!"
            elif score_difference > 5:
                alert = f"{game[f'team{i}']} scored a touchdown!"
            else:
                alert = f"{game[f'team{i}']} scored {score_difference} points!"
            return alert
    return None
            

def print_game(game):
    return f'{game["team0"]}: {game["score0"]} {game["status"]}\n{game["team1"]}: {game["score1"]}'


if __name__ == "__main__":
    main()