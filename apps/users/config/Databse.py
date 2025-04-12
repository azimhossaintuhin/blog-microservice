TORTOISE_ORM = {
    "connections": {"default": "mysql://mysql:mysql@user-db:3306/users_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
        
    },
}