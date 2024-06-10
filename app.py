from query import invoke


def run():
    while True:
        query = input("your query:")
        sources, answer = invoke(query)
        print(answer)
        print("Sources")
        for source in sources:
            print(source)


if __name__ == "__main__":
    run()
