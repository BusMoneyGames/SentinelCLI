import requests
def send_build_message():
    path = "https://hooks.slack.com/services/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"

    msg = {"attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#2eb886",
            "pretext": "Sentinel - Daily Report",
            "author_name": "View Report",
            "author_link": "https://s3-eu-west-1.amazonaws.com/bmg-parity-sentinel/index.html",
            "title": "Build Link",
            "title_link": "https://d1zmsx0ic945r7.cloudfront.net/IslandOfWinds.zip"
        }
    ]}

    requests.post(path, json=msg)

