TORTOISE_ORM = {
    "connections": {"default": "mysql://mysql:mysql@commet-db:3306/comments_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
        
    },
}