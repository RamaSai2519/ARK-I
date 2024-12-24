import os

if __name__ == "__main__":
    os.system("gunicorn app:app -b 0.0.0.0:5000 -w 3")
