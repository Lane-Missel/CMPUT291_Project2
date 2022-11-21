from pymongo import MongoClient
import sys

class DatabaseManager:

    def __init__(self, port: int):
        self.client = MongoClient()

    def search_articles(self, keywords: list[str]) -> list[dict[str: str, str: str, str: list[str]], str: str, str: str, str: int]:
        """
        Returns all articles that have a keyword in the title, authors, abstract, venue or year.
        The return will be a list of dictionaries in the format:
            {'id': <str>,
            'title': <str>,
            'authors': [<str>,],
            'abstract': <str>,
            'venue': <str>,
            'year': <int>}1
        """

    def search_authors(self, keyword: str) -> list[list[str, int]]:
        """
        Returns all authors whose name includes the provided keyword.
        in form [[<author1>,<publications>],]
        """
        assert(len(keyword) > 0)
        assert(isinstance(keyword, str))

    def top_venues(self, n: int):
        """
        Returns the top n venues, based on the number of articles that reference the venue.
        The return will be a list of dictionaries in the format:
            [[<venue1>, <BiggestArticleCount>], [<venue2>, <SmallerArticelCount>]]
        """
        assert(n > 0)
        assert(isinstance(n, int))

    def add_article(self, identifier: str, title: str, authors: list[str], year: int):
        """
        Adds an article to the mongo database.
        """

class Interface:

    def __init__(self, database: MongoClient):
        self.database = database

    def selection(self):
        """
        Return int repersenting users selection.
        """
        print("[0] Close Program")
        print("[1] Search for articles")
        print("[2] Search for authors")
        print("[3] List the venues")
        print("[4] Add an article")
        user_input = input("Enter your selection: ")

        try:
            user_input = int(user_input)
        except Exception:
            return -1

        if user_input in range(0,4):
            return user_input

        return -1

    def search_for_articles(self):
        # prompt for keywords
        keywords = input("Enter keywords: ").strip().split()

        if len(keywords) < 1:
            print("No keywords entered. Returning to main.")
            return

        articles = self.database.search_for_articles(keywords)

        if len(articles) == 0:
            print("No articles found containing keywords: ", end="")
            
            for keyword in keywords:
                print(keyword, end=" ")

            return

        # display articles (allow user to pick them)...  

    def search_for_authors(self):
        pass

    def list_the_venues(self):
        pass

    def add_an_article(self):
        pass

    def run(self):
        print("Welcome!")

        running = True

        while running:
            selection = self.selection()

            if selection == -1:
                print("Invalid option selected... Try again.")
                
            elif selection == 0:
                print("Exiting program... Goodbye.")
                running = False

            elif selection == 1:
                self.search_for_articles()

            elif selection == 2:
                self.search_for_authors()

            elif selection == 3:
                self.list_the_venues()

            elif selection == 4:
                self.add_an_article()

            else:
                print("Entry error. Try again...")

if __name__ == '__main__':
    port = sys.argv[1]

    try:
        port = int(port)
    except Exception:
        print("Invalid port number. Exiting...")
        exit()

    database = DatabaseManager(port)
    interface = Interface(database)
    interface.run()