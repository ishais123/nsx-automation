import requests

URL = "https://www.one.co.il/"
def main():
    response = requests.get(URL)
    print(response.text)

if __name__ == '__main__':
    main()