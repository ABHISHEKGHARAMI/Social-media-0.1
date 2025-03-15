from pydantic import BaseSettings

# class for the config for credentials for different things
class Settings(BaseSettings):
    database_name : str
    database_hostname : str
    database_port : str
    database_username : str
    database_password : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    
    # setting up the env file
    class Config:
        env_file = '.env'
    
    
    
# creating the instance of the settings class
settings = Settings()