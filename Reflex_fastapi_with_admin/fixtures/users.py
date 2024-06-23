users = [
    {"admin": {
        "name": "Administrator",
        "avatar": "avatar.png",
        "company_logo_url": "avatar.png",
        "roles": ["read", "create", "edit", "delete", "action_make_published"],
        }
    },
    {"johndoe": {
        "name": "John Doe",
        "avatar": None,  # user avatar is optional
        "roles": ["read", "create", "edit", "action_make_published"],
        },
    },
    {"viewer": {"name": "Viewer", "avatar": None, "roles": ["read"]},}
]