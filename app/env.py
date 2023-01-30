from environs import Env

# move this to a file such that every import has the env loaded
env = Env()
env.read_env()  # read .env file, if it exists
