import os
from dotenv import load_dotenv


load_dotenv()

x = os.getenv("DVLA_API_KEY")


print(x)