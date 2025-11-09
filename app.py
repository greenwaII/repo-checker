import os
from json import JSONDecodeError
from typing import List, Optional

import requests
from flask import Flask, render_template, request


class RobloxAPIError(Exception):
    """Raised when the Roblox API returns an application-level error."""


app = Flask(__name__)

ROBLOX_FRIENDS_API = "https://friends.roblox.com/v1/users/{user_id}/friends"


def fetch_friends(user_id: str) -> List[dict]:
    """Fetch a Roblox user's friends from the public API."""
    url = ROBLOX_FRIENDS_API.format(user_id=user_id)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    try:
        payload = response.json()
    except JSONDecodeError as exc:  # pragma: no cover - defensive branch
        raise requests.RequestException("Invalid JSON in Roblox response") from exc
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first_error = errors[0]
            message = first_error.get("message") if isinstance(first_error, dict) else None
            raise RobloxAPIError(message or "Roblox returned an error response.")
    return payload.get("data", [])


@app.route("/", methods=["GET", "POST"])
def index():
    user_id: str = ""
    friends: List[dict] = []
    error: Optional[str] = None

    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()

        if not user_id:
            error = "Please enter a Roblox user ID."
        elif not user_id.isdigit():
            error = "The Roblox user ID must be a number."
        else:
            try:
                friends = fetch_friends(user_id)
                if not friends:
                    error = "No friends found for that user ID."
            except RobloxAPIError as exc:
                error_message = str(exc)
                error = error_message or "Roblox returned an error response."
            except requests.HTTPError as exc:
                if exc.response.status_code == 404:
                    error = "Roblox user not found."
                else:
                    error = "Failed to fetch friends from Roblox."
            except requests.RequestException:
                error = "Unable to contact the Roblox API. Please try again later."

    return render_template("index.html", user_id=user_id, friends=friends, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
