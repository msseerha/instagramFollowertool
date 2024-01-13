import os.path
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def combinelist2dict (list1, list2):
    return dict(zip(list1,list2))

def string2dateinList(l): 
    Followerdatelist = []
    for x in l:
        dateformat = '%b %d, %Y, %I:%M %p'
        date_obj = datetime.strptime(x, dateformat)
        Followerdatelist.append(date_obj)
    return Followerdatelist

pathFollowerhtml = 'followers_and_following/followers_1.html'
pathFollowinghtml = 'followers_and_following/following.html'

quitCommand = False

Initialcommand = input("Welcome to the Instagram Follower Analysis Tool. Type 'Y' to proceed:")

while (True):
    if quitCommand == True:
        print("Program close, please launch it again")
        break
    
    elif Initialcommand == 'Y':
        print ("\nChecking for files...")
        
        if (os.path.isfile(pathFollowinghtml) and os.path.isfile(pathFollowerhtml)):
            try:
                follower_fileraw = open("followers_and_following/followers_1.html", "r")
                follower_raw = follower_fileraw.read()
                followerslist = re.findall(r"<a.*?>(.*?)</a>",follower_raw)

                following_fileraw  = open("followers_and_following/following.html", "r")
                following_raw = following_fileraw.read()
                followinglist = re.findall(r"<a.*?>(.*?)</a>",following_raw)
                  

                followers_timestamp_raw = re.findall(r"<div>(.*?)</div>",follower_raw)
                followersdate_extractor = re.compile(r"[A-z]{3}[ ]\d+,[ ]\d{4},[ ]\d+:\d+[ ][A-Z]{2}")
                followerstimestamp = sum([followersdate_extractor.findall(x) for x in followers_timestamp_raw],[])
                dictFollowerdetail = combinelist2dict(followerslist,followerstimestamp)      
                followerstimestamp2 = string2dateinList(followerstimestamp)
                dictFollowerdetail2 = combinelist2dict(followerslist,followerstimestamp2)

                followerSet = set(followerslist)
                followingSet = set(followinglist)
                intersectionSet = followingSet.intersection(followerSet)
                notfollowyouSet = followingSet - intersectionSet
                younotfollowSet = followerSet - intersectionSet

                uniqueyearlist = []
                uniqueyearmonthdict = {}
                uniqueyearcountdict = {}
                ##uniquemonthcountdict = {}
                for x in dictFollowerdetail2:
                    if dictFollowerdetail2[x].year not in uniqueyearmonthdict.keys():
                        uniqueyearmonthdict[dictFollowerdetail2[x].year] = [dictFollowerdetail2[x].month]
                        uniqueyearcountdict[dictFollowerdetail2[x].year] = 1
                    else:
                        uniqueyearmonthdict[dictFollowerdetail2[x].year].append(dictFollowerdetail2[x].month)
                        uniqueyearcountdict[dictFollowerdetail2[x].year] += 1
                    uniqueyearmonthdict[dictFollowerdetail2[x].year].sort()

                year = list(uniqueyearcountdict.keys())
                followerCount = list(uniqueyearcountdict.values())


                print ("Files are found.") 
                print ("\nAs per these files: \n"
                       "Your total number of followers are: "+ str(len(followerslist)) + "\n"
                       "You are following " + str(len(followinglist)) + " users\n")            

                while (True):
                    print  ("\nYou can use this tool, to get the following information:\n"
                            "1. Get follower information on when they first started following you.\n"
                            "2. Get a list of userIDs that do not follow you back.\n"
                            "3. Get a list of userIDs that you do not follow back.\n"
                            "4. Get a list of userIDs that started following you, in a specified period.\n"
                            "5. Track follower count a) by year or, b) by month.\n"
                                    "You can press 'Q' to quit the program")

                    PickOption = input ("Select the number between 1-5 from above listed options, for the information you seek.")

                    match PickOption:
                        case "1":
                            print ("\nYou have selected: 1. Get follower information on when they first started following you.")
                            usernameEnter = input("\nEnter user name of person you would like to know when they followed you:")
                            if usernameEnter in dictFollowerdetail.keys():
                                print("User '" + usernameEnter + "' started following you on " + dictFollowerdetail[usernameEnter])
                            else:
                                print ("ERROR: Invalid username or this user does not follow you.")

                        case "2":
                            print ("\nYou have selected: 2. Get a list of userIDs that do not follow you back.")
                            print ("\nOut of "+ str(len(followingSet)) + " users you follow, only " + str((len(followingSet)-len(notfollowyouSet))) + " follows you back.")
                            print (str(len(notfollowyouSet)) + " users who do not follow you are: \n")
                            for x in notfollowyouSet:
                                print (x)

                        case "3":
                            print ("\nYou have selected: 3. Get a list of userIDs that you do not follow back.")
                            print ("\nThese are the " + str(len(younotfollowSet)) + " people that follow you, but you don't, they are listed below:\n")
                            for x in younotfollowSet:
                                print (x)

                        case "4":
                            try:
                                counter = 0
                                print ("\nYou have selected: 4. Get a list of userIDs that started following you, in a specified period.")
                                start_date = datetime.strptime(input("\nStart Date (in format YYYY-MM-DD)"), '%Y-%m-%d')
                                end_date = datetime.strptime(input("End Date (in format YYYY-MM-DD)"), '%Y-%m-%d')
                                print ("\n")

                                for user, date in dictFollowerdetail2.items():
                                    if start_date <= date <= end_date:
                                        counter += 1
                                        print (user + " followed you on " + str(date))

                                print ("\nYou had total of " + str(counter) + " followers during the period " + str(start_date) + " to " + str(end_date) + " .")
                            except ValueError:
                                print ("Wrong date format please try again and make sure you enter both dates in format YYYY-MM-DD.")

                        case "5":
                            print ("\nYou have selected: 5. Track follower count a) by year or, b) by months")
                            choice = input ("Input 'a' to do by year or 'b' to do by months\n")
                            match choice:
                                case "a":
                                    plt.bar(year,followerCount)
                                    plt.title("Follower Count over the years")
                                    plt.xlabel("Year")
                                    plt.ylabel("Follower Count")
                                    plt.show()

                                case "b":
                                    plt.xlabel("Month")
                                    plt.xticks(np.linspace(1,12,12))
                                    plt.ylabel("Follower Count")
                                    plt.title("Follower Count over the months for all years")
                                    plt.hist(uniqueyearmonthdict.values())
                                    plt.legend(uniqueyearmonthdict.keys())
                                    plt.show()

                                    choiceYear = input("if you want to do by specific year, please input the year in format YYYY or input 'Q' to go back")
                                     
                                    if choiceYear == 'Q':
                                        continue
                                    
                                    else:
                                        try:
                                            if int(choiceYear) in uniqueyearmonthdict.keys():
                                                plt.xlabel("Month")
                                                plt.xticks(np.linspace(1,12,12))
                                                plt.ylabel("Follower Count")
                                                plt.title("Follower Count over the months for " + choiceYear)
                                                plt.hist(uniqueyearmonthdict[int(choiceYear)])
                                                plt.show()
                                        except:
                                            print ("ERROR: Invalid Year/No Data for Year")

                                case _:
                                    print ("ERROR: Invalid Entry")
                                    
                        case "Q":
                            quitCommand = True
                            break
                        case _:
                            print ("Invalid Input")
            except:
                print ("ERROR: Invalid format of files. Make sure they are both html then try again.")
                follower_fileraw.close()
                following_fileraw.close()
                break
        
        else:
            print ("ERROR: followers_1.html & following.html are not to be found in the 'followers_and_following' folder in the same directory as this program. Please run this program again after you get the files and make sure they are in the correct directory")
            break
    
    else:
        print ("ERROR: Wrong Command")
        Initialcommand = input ("Please press 'Y' to proceed.")
        