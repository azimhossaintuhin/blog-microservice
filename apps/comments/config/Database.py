TORTOISE_ORM = {
    "connections": {"default": "mysql://mysql:mysql@comments-db:3306/comments_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
        
    },
}