from dataclasses import dataclass

from flask import Flask, request, jsonify, make_response
from tinydb import TinyDB, where, Query

app = Flask(__name__)
db = TinyDB("db.json")


Reward = Query()


@dataclass
class BonusReward:
    name: str
    code: str


def to_dict(reward: BonusReward) -> dict[str, str]:
    return {"name": reward.name, "code": reward.code}


@app.route("/")
def root():
    return jsonify(name="Lyubo")


@app.route("/insert/<name>/<code>", methods=["POST"])
def insert(name, code):
    current_reward = BonusReward(name, code)
    db.insert(to_dict(current_reward))

    return jsonify(result="OK")


@app.route("/reward/<name>")
def get(name):
    return jsonify(result="OK", rewards=db.search(Reward.name == name))


@app.route("/remove/<code>", methods=["DELETE"])
def remove(code):
    matching = db.search(Reward.code == code)

    if len(matching) == 0:
        # 404
        return make_response(jsonify(result="Not found"), 404)

    db.remove(Reward.code == code)

    return jsonify(result="OK")
