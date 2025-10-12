# app.py
from flask import Flask, jsonify
from AI.agent import Prompt_Taker

app = Flask(__name__)

@app.route('/<prompt>', methods=['GET'])
def main(prompt):
    result = Prompt_Taker(prompt)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
