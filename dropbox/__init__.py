from . import dropbox

Stream = dropbox.DropboxTeam

CONFIG = {
    "title": "Dropbox Team",
    "icon": "data:image/png;base64,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",
    "params": [
        {
            "name": "token",
            "required": True,
            "title": "Access Token",
            "type": "password",
            "help": "Your Dropbox Team access token.",
            "link": "https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/"
        },
        {
            "name": "endpoints",
            "required": True,
            "type": "list",
            "values": map(lambda e: e["uri"], dropbox.ENDPOINTS),
            "dependencies": ["token"]
        },
        {
            "name": "destination",
            "required": True,
            "dependencies": ["token"],
            "default": "hello"
        }

    ],
    "categories": [ "API" ],
    "keywords": [ "events", "team", "audit" ],
    "createdAt": "2016-10-21"
}