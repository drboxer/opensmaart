import json


def save_session(
        file,
        data
):

    with open(
            file,
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def load_session(
        file
):

    with open(
            file,
            "r",
            encoding="utf-8"
    ) as f:

        return json.load(
            f
        )