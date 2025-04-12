TORTOISE_ORM = {
    "connections": {"default": "mysql://mysql:mysql@blog-db:3306/blogs_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
        
    },
}