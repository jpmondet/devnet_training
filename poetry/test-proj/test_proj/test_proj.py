import requests


def main():
    r = requests.get("https://api.chucknorris.io/jokes/random").json()
    print(r['value'])


if __name__ == "__main__":
    main()
