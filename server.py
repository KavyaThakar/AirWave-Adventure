from flask import Flask, jsonify, render_template, request
import threading
import subprocess

app = Flask(__name__)

# Flag to check if the game is running
game_running = False
game_over = False
final_score = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    global game_running, game_over
    if not game_running and not game_over:
        threading.Thread(target=run_game).start()
        return jsonify({"status": "Game started!"}), 200
    elif game_running:
        return jsonify({"status": "Game is already running!"}), 400
    else:
        return jsonify({"status": "Game over. Restart to play again."}), 400

def run_game():
    global game_running
    game_running = True
    subprocess.call(["python", "game1.py"])  # Start the game script
    game_running = False

@app.route('/game-over', methods=['POST'])
def game_over_route():
    global game_over, final_score
    data = request.get_json()
    final_score = data.get("score", 0)
    game_over = True
    return jsonify({"status": "Game Over!"}), 200

@app.route('/game-over-page')
def game_over_page():
    return render_template('game_over.html', score=final_score)

if __name__ == '__main__':
    app.run(debug=True)
