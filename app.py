<<<<<<< HEAD
# app.py
from flask import Flask, jsonify
from AI.agent import Prompt_Taker

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the AI Command Generator API. Use /<your_prompt> to get started."

@app.route('/<prompt>', methods=['GET'])
def main(prompt):
    result = Prompt_Taker(prompt)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

=======
# app.py
from flask import Flask, jsonify
from AI.agent import Prompt_Taker

app = Flask(__name__)

@app.route('/<prompt>', methods=['GET'])
def main(prompt):
    result = Prompt_Taker(prompt)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

>>>>>>> 6490dfc476815c45cd8cfeca3c900e84e26d3b75
