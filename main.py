# main.py
import uvicorn
from app.utils.env_utils import EnvironmentVariable, get_env

if __name__ == "__main__":
    host = get_env(EnvironmentVariable.HOST, "127.0.0.1")
    port = int(get_env(EnvironmentVariable.PORT, "10000"))
    uvicorn.run("app.app:app", host=host, port=port, reload=True)
