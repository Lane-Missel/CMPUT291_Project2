from pymongo import MongoClient
import sys
from typing import List,Dict

class DatabaseManager:

    def __init__(self, port: int):
        self.client = MongoClient("mongodb://localhost:{}".format(port))
        self.collection = self.client.get_database("291db").get_collection("dblp")

    def search_articles(self, keywords: list[str]) -> List[Dict[str: str, str: str, str: List[str], str: str, str: str, str: int]]:
        """
        Returns all articles that have a keyword in the title, authors, abstract, venue or year.
        The return will be a list of dictionaries in the format:
            {'id': <str>,
            'title': <str>,
            'venue': <str>,
            'year': <int>}
        """
        #self.collection.createIndex( {id: "text", title: "text", venue: "text", year: "text"} )
        keywords = ' '.join(keywords)
        return list(self.collection.find( {'$text': { '$search': keywords } } ))
        #return [{"id": "AAAABBBB", "title": "Test Paper", "venue": "Big Test Venue", "year": 2022}, {"id": "DDDDBBBB", "title": "Another Test Paper", "venue": "Another Test Venue", "year": 2018}]

    def search_authors(self, keyword: str) -> List[List[str, int]]:
        """
        Returns all authors whose name includes the provided keyword.
        in form [[<author1>,<publications>],]
        """
        assert(len(keyword) > 0)
        assert(isinstance(keyword, str))

        self.collection.find({"id": "/.*{}.*/i".format(keyword)})

        return [["Test Author", 22], ["Another Author", 10]]

    def top_venues(self, n: int):
        """
        Returns the top n venues, based on the number of articles that reference the venue.
        The return will be a list of dictionaries in the format:
            [[<venue1>, <BiggestArticleCount>, <ReferenceCount>], [<venue2>, <SmallerArticelCount>, <RefercenCount>]]
        """
        assert(n > 0)
        assert(isinstance(n, int))

        # aggregate base on venue -- still need to count how many times the venue is indirec;y referenced.
        result = self.collection.aggregate([{"$group": {"_id": "$venue", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}]).limit(n)

        return_list = []        
        # subquery to get teh reference counts
        for document in result[:n]:
            return_list.append(document)
            result2 = self.collection.aggregate([{"$match": {"references": document["id"]}}, {"$count": "referenceCount"}])
            document["referenceCount"] = result2[0]["referenceCount"]
            return_list.append(document)

        return return_list

    def add_article(self, identifier: str, title: str, authors: list[str], year: int):
        """
        Adds an article to the mongo database.
        """
        if self.has_key(identifier):
            raise KeyError
        
        self.collection.insert({"id": identifier, "title": title, "authors": authors, "year": year, "abstract": None, "venue": None, "references": [], "n_citations": 0})

    def find_article(self, article_id: str) -> dict:
        """
        return dictionary containing information of article with provided id.
        """
        return self.collection.find({"id": article_id})

    def articles_by_author(self, author: str) -> List[dict]:
        """
        title, venue, and year (sorted by year descending)
        """
        return [["Test Paper", "A Big Venue", 2022],["Another Paper", "Smaller Venue", 2017]]

    def has_key(self, key: str) -> bool:
        result = self.collection.find({"id": key}) == 1
        try:
            return result[0] is not None
        except Exception:
            return False

class Interface:

    def __init__(self, database: DatabaseManager):
        """
        Author: Lane Missel
        """
        self.database = database
        self.collection = self.database["dblp"]

    def selection(self):
        """
        Author: Lane Missel
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
        """
        Author: Lane Missel
        """
        # prompt for keywords
        keywords = input("Enter keywords: ").strip().split()

        if len(keywords) < 1:
            print("No keywords entered. Returning to main.")
            return

        articles = self.database.search_articles(keywords)

        if len(articles) == 0:
            print("No articles found containing keywords: ", end="")
            
            for keyword in keywords:
               print(keyword, end=", ")

            return

        # display articles (allow user to pick them)...
        print("{} {} {} {} {}".format(" ", "id", "title", "year", "venue"))
        
        num_articles = len(articles)

        for i in range(num_articles):
            article = articles[i]
            print("entry: {}".format(i+1))
            print("id: {}".format(article['id']))
            print("title: {}".format(article['title']))
            print("year: {}".format(article['year']))
            print("venue: {}".format(article['venue']))
            print("- - " * 5)

        valid_choice = False
        while not valid_choice:
            user_input = input("Enter entry number for the artice you would like to choose (or 0 to exit): ")

            article_index = None
            try:
                article_index = int(user_input) - 1
            except Exception:
                print("Invalid entry. Try again.")

            if article_index in range(num_articles):
                valid_choice = True

        article_id = articles[article_index]["id"]
        article = self.database.find_article(article_id)

        # Display the choosen article:
        print("Article with id: {}".format(article["id"]))
        print("title: {}".format(article["title"]))
        print("year: {}".format(article['year']))
        print("venue: {}".format(article["venue"]))
        print("authors: ", end="")
        
        for author in article["authors"]:
            print(author, end=" ")

        print("references:")

        for ref_article_id in article["references"]:
            print("Article with id {}:".format(ref_article_id))
            ref_article = self.database.find_article(ref_article_id)
            print("title: {}".format(ref_article_id))
            print("year: {}".format(ref_article["year"]))
            print("* *" * 5)

        return

    def search_for_authors(self):
        """
        Author: Lane Missel
        """
        keyword = input("Enter keyword: ").strip()

        if len(keyword) == 0:
            print("No keyword entered.")
            return

        authors = self.database.search_authors(keyword)

        if len(authors) == 0:
            print("No authors found.")
            return

        print("[0] Return to menu")
        num_authors = len(authors)
        for i in range(num_authors):
            author = authors[i]
            print("[{}] {} - {} publications".format(i + 1, author[0], author[1]))

        valid_selection = False
        while not valid_selection:
            selection = input("Selection: ").strip()

            if len(selection) == 0:
                print("No artist selected. Try again.")
                continue

            try:
                author_index = int(selection) - 1
            except Exception:
                print("Invalid selection. Try again.")
                continue

            if author_index not in range(-1, num_authors):
                print("Invalid selection. Try again.")
                continue

            valid_selection = True

        # display selected author.            
        if author_index < 0:
            return

        # display publications by author
        for entry in self.database.articles_by_author(authors[author_index][0]):
            print("{} - {} - {}".format(entry[0], entry[1], entry[2]))
        
    def list_the_venues(self):
        """
        Author: Lane Missel
        """
        valid_number = False
        while not valid_number:
            try:
                num_venues = int(input("Top n venues? ").strip())
            except Exception:
                print("invalid selection. Try again.")

            if num_venues < 1:
                print("cannot return negive amount of venues. Back to home.")
                return

            valid_number = True

        # get venues
        venues = self.database.top_venues(num_venues)

        for i in range(len(venues)):
            venue = venues[i]
            print("{}. {} hosted {} articles and references {}".format(i+1, venue["_id"], venue["count"], venue["referenceCount"]))

        return

    def add_an_article(self):
        """
        Author: Lane Missel
        """
        unique_id = input("Enter id: ")
        
        if self.database.has_key(unique_id):
            print("This id already exists. Back to Home.")
            return

        title = input("Title: ")

        if len(title) < 1:
            print("Title cannot be empty. Back to Home")
            return

        authors = input("Authors: ").split(",")
        
        if len(authors) < 1:
            print("Must be atleast one author. Bc to Home.")
            return

        year = input("Year: ")
        try:
            year = int(year)
        except Exception:
            print("Invalid year entered. Back to Home.")

        self.database.add_article(unique_id, title, authors, year)

    def run(self):
        """
        Author: Lane Missel
        """
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
    port = sys.argv[2]

    try:
        port = int(port)
    except Exception:
        print("Invalid port number. Exiting...")
        exit()

    database = DatabaseManager(port)
    interface = Interface(database)
    interface.run()
