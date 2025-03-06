import os

import uvicorn

import init


def main():
    if not os.path.isfile(".instance/mchat.db"):
        init.main()
    uvicorn.run("mchat.main:app", reload=True)


if __name__ == "__main__":
    main()
