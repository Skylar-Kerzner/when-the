from environs import Env

env = Env()
env.read_env()


with env.prefixed("WHEN_THE_"):
    logging_level = env("LOGGING_LEVEL", "INFO")