import uvicorn


def main():
    uvicorn.run("mchat.main:app", reload=True)


if __name__ == "__main__":
    main()
