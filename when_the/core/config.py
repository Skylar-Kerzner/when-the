from environs import Env

env = Env()
env.read_env()


with env.prefixed(""):
    logging_level = env("LOGGING_LEVEL", "DEBUG")
    app_secret_key = env("APP_SECRET_KEY", "vkjhasjkdhdsa")
