# solve the recommender problem  # NOTE: this is NOT good style; each step should be a function called by main() with appropriate parameters
# STEP1: create list (from a set) of all the book titles
# open the file getting name of file from command line arguments
# make sure user has given correct number of arguments
import sys

def main():
    #python read file from command line argument and put each line into a list
    if len(sys.argv) != 2:
        print("USAGE: python recommend2.py filename")
        quit()
    ratingsFile = open(sys.argv[1], "r")
    lines = ratingsFile.readlines()

    #Construct the list of books and a dictionary of users=ratings
    booklist = getbooks(lines)
    emptyDict = getdict(lines, booklist)
    ratingsDict = getratings(lines, booklist, emptyDict)

    #calculate average scores
    avgs = averages(booklist, ratingsDict)

    #Take input from user and output results
    print("Welcome to the CSCI 236 Book Recommender. Type the word in the")
    print("left column to do the action on the right.")
    print("recommend : recommend books for a particular user")
    print("averages  : output the average ratings of all books in the system")
    print("quit      : exit the program")
    task = input("next task?").lower()
    while task != "quit":
        if task == "averages":
            for average in avgs:
                title = average[1]
                score = average[0]
                print(title + " " + str(score))
            task = input("\nnext task?").lower()
        elif task == "recommend":
            targetUser = input("user?")
            if targetUser not in ratingsDict.keys():
                for average in avgs:
                    print(str(average)[1:-1])
                task = input("\nnext task?").lower()
            else:
                compareList = similaritylist(ratingsDict, targetUser)
                recommendList = recommend(compareList, booklist, ratingsDict)
                for recommendation in recommendList:
                    bookTitle = recommendation[0]
                    bookRating = recommendation[1]
                    print(bookTitle + " " + str(bookRating))
                task = input("\nnext task?").lower()
#find recommendations for the selected user based on the average ratings of the top 3 similar users
def recommend(comparelist, books, ratings):
    newList = [0] * len(books)
    recommendations = []
    user1 = comparelist[0][1]
    user2 = comparelist[1][1]
    user3 = comparelist[2][1]

    for i in range(0, len(newList)):
        x = 0
        if ratings[user1][i] != 0:
            x += 1
        if ratings[user2][i] != 0:
            x += 1
        if ratings[user3][i] != 0:
            x += 1
        if x != 0:
            newList[i] = (ratings[user1][i] + ratings[user2][i] + ratings[user3][i])/x
        else:
            newList[i] = 0
    for i in range(0, len(newList)):
        rTuple = (books[i], newList[i])
        if rTuple[1] > 0:
            recommendations.append(rTuple)
    recommendations.sort(key=lambda a: -a[1])
    return recommendations



#generate list of similarity scores to the selected user
def similaritylist(ratings, myUser):
    simList = []
    for users in ratings.keys():
        simScore = 0
        for i in range(0, len(ratings[myUser])):
            simScore += (ratings[myUser][i] * ratings[users][i])
        if users != myUser:
            simList.append((simScore, users))
    simList.sort(reverse=True)
    return simList



#Loop through list of books and calculate/return a list of tuples containing the book and it's average rating
def averages(books, ratings):
    avgList = []
    for i in range(0, len(books)):
        currentbook = books[i]
        total = 0
        ratingCount = 0
        for user in ratings.keys():
            total += ratings[user][i]
            if ratings[user][i] != 0:
                ratingCount += 1
        avgTuple = (total / ratingCount, currentbook)
        avgList.append(avgTuple)
    avgList.sort(reverse=True)
    return avgList

#Loop through the list of lines and put each book title into a list
def getbooks(lineList):
    books = set()
    for lineCount in range(0, len(lineList)-1, 3):
        books.add(lineList[lineCount+1].rstrip())
    books = list(books)
    return books

#Loop through the lines of the file and put each user into a set, then loop through the set and put each user and
# an empty list into a dictionary
def getdict(lineList, books):
    users = set()
    zeroRatings = [0]*len(books)
    ratingsDict = dict()
    for lineCount in range(0, len(lineList)-1, 3):
        users.add(lineList[lineCount].rstrip())
    for user in users:
        ratingsDict[user] = zeroRatings.copy()
    return ratingsDict

#Loop through the lines of the file and the list of books, match the user and the book ratings, and input the rating
# into the complete dictionary
def getratings(lineList, books, mydict):
    newDict = mydict.copy()

    for lineCount in range(0, len(lineList)-1, 3):
        for i in range(0, len(books)):
            sourceBook = lineList[lineCount + 1].strip()
            targetBook = books[i]
            if sourceBook == targetBook:

                myKey = lineList[lineCount].strip()
                newDict[myKey][i] = int(lineList[lineCount + 2].strip())
    return newDict

main()
