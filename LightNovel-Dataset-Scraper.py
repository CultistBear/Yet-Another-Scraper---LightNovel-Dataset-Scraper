from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
import time 
import os

os.system("color")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

Results_Link=[]
Results_Titles=[]
Status=[]

#Function takes the input of the series to search
def Start():
    Series_Name = input("\033[1;31mEnter the name of Light Novel series to search: \033[0;37m")
    Results_Link.clear()
    Results_Titles.clear()
    Series_Search(Series_Name)

#Function Searches the series through NovelUpdates Database
def Series_Search(Series_Name):
    Scraper = cloudscraper.create_scraper(delay=6)
    print("\033[1;32m \nWaiting for Cloudfare... \033[0;37m \n")

    if Series_Name.isspace:
        Series_Name=Series_Name.replace(" ", "+")

    Search_Results=Scraper.get("https://www.novelupdates.com/?s=%s&post_type=seriesplans" %(Series_Name),stream=True)
    Soup=BeautifulSoup(Search_Results.content, "html.parser")

    print("\033[1;32mSearching...\033[0;37m \n")
    try:
        for Results in Soup.find("div", class_="w-blog-list").findAll("a",{'class':''}, href=True):
            Results_Link.append(Results['href'])
            Results_Titles.append(Results.string)
            if len(Results_Link)==10:
                break

    except AttributeError:
        print("\033[1;31mThere were no results, Please check the spelling and try again. \033[0;37m\n")
        print("\n"*5)
        time.sleep(2)
        Start()
    else:
        Listing()

#Function just lists all the available titles recieved after searching, this is done just to make the After_Search_Action_Menu function look better
def Listing():
        if len(Results_Link)==1:
            print("\033[1;32mHere is the top result:\033[0;37m \n")
        else:
            print("\033[1;32mHere are the top %i results: \033[0;37m\n" %(len(Results_Link)))
        for i in Results_Titles:
            print(i,"\n")
        After_Search_Action_Menu()

#Function takes the input of the user choice after listing all the series after search.
def After_Search_Action_Menu():
    try:
        After_Search_Action_Menu.Choice=int(input('''\033[1;31mDo you wish to
    
        1) Read the description of one of the series mentioned above
        2) Search another series
        3) Exit
    
Pick one: \033[0;37m'''))
        
    except (ValueError, TypeError):
        print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
        time.sleep(2)
        Listing()
    
    else:
        if int(After_Search_Action_Menu.Choice)==1:

            #Function lists all the titles with index for user to select which novel to show the description of. Exists to make the program look a bit better.
            def Desc_Show():
                for i in Results_Titles:
                    print("\n[",Results_Titles.index(i)+1,"]:",i)
                print()
                try:
                    Choice_Desc=int(input("\033[1;31mPlease enter the index number of the series you wish to see the description of: \033[0;37m"))
                except (ValueError, TypeError):
                    print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
                    time.sleep(2)
                    Desc_Show()
                else:
                    if 0<Choice_Desc<=len(Results_Titles):
                        Fetch_Novel_Desc(Results_Link[Choice_Desc-1])
                    else:
                        print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
                        time.sleep(2)
                        Desc_Show()
            Desc_Show()
        elif int(After_Search_Action_Menu.Choice)==2:
            print("\n"*50)
            Start()
        elif int(After_Search_Action_Menu.Choice)==3:
            exit()
        else:
            print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
            time.sleep(2)
            Listing()

#Function Prints all the relevant data from the NovelUpdates site after scraping  
def Fetch_Novel_Desc(Fetch_Link):
    Scraper = cloudscraper.create_scraper(delay=6)
    Fetch_Page=Scraper.get(Fetch_Link)
    Soup=BeautifulSoup(Fetch_Page.content,"html.parser")

    #Print the Title
    print("\n\033[1;96mTitle\n\033[0;37m","",Soup.find("div",class_="seriestitlenu").string)

    #Print the Description
    print("\n\033[1;96mDescription\033[0;37m")
    Desc_Para_List = Change(Soup.find("div",id="editdescription"))
    for i in Desc_Para_List:
        if "\n" in i: 
            i=i.replace("\n","")
        print(" ",i,"\n") 
    Status.clear()

    #Print the Genre
    print("\033[1;96mGenre\033[0;37m")
    for Desc_Genre in Soup.find("div", id="seriesgenre").findAll("a"):
        print(" ",Desc_Genre.string,end=',')

    #Print the Rating
    print("\n\n\033[1;96mRating\033[0;37m\n ", Soup.find("span", class_="uvotes").string.replace("(","").replace(")",""))
    
    #Print Status In COO (Country of Origin)
    print("\n\033[1;96mStatus in Country of Origin\033[0;37m")
    Desc_Status=Change(Soup.find("div", id="editstatus"))
    for i in Desc_Status:
        if "\n" in i:
            i=i.replace("\n","")
        print(" ",i)
    Status.clear()

    #Print Translation
    print("\n\033[1;96mCompletely Translated\033[0;37m\n ",end='')
    Desc_Transated=Soup.find("div",id="showtranslated") 
    if Desc_Transated.find('a') !=None: 
        print("",Desc_Transated.find('a').string.replace("\n",""))
    else:
        print("",Desc_Transated.string.replace("\n",""))

    #Print Associated Names
    print("\n\033[1;96mAssociated Names\033[0;37m")
    Desc_Asso_Names=Change(Soup.find("div", id="editassociated"))
    for i in Desc_Asso_Names:
        if "\n" in i: 
            i=i.replace("\n","")
        print(" ",i) 
    Status.clear()

    #Print Related Series
    print("\n\033[1;96mRelated Series\033[0;37m")
    Count=0
    Names=[]
    Type_Related=[]
    for Series in Soup.find("div",class_="two-thirds").find('div', class_= 'wpb_wrapper').findAll('a',class_='genre',href=True):
        if (Series.get("title")==None):
            Count=1
            Names.append(Series.string)
            if "\n" in Series.next_sibling:
                Next_Sibling=Series.next_sibling.replace("\n","")
                Type_Related.append(Next_Sibling)
            else:
                Type_Related.append(Series.next_sibling)
        elif (Series.get("title")!=None):
            continue
    if Count==0:
        print("  None")
    else:
        print(pd.DataFrame({"  ":Names," ":Type_Related}).to_string(index=False))

    #Print Recommendations
    print("\n\033[1;96mRecommendations\033[0;37m")
    Count=0
    Names=[]
    Rec_Votes=[]
    for Series in Soup.find("div",class_="two-thirds").find('div', class_= 'wpb_wrapper').findAll('a',class_='genre',href=True):
        if (Series.get("title")!=None):
            Count=1
            Names.append(Series.string)
            Rec_Votes.append(Series.get("title"))
        elif (Series.get("title")==None):
            continue
    if Count==0:
        print("  None")
    else:
        print(pd.DataFrame({"  ":Names," ":Rec_Votes}).to_string(index=False))

    #Print Choice Menu
    try:
        Fetch_Novel_Desc.Choice=int(input('''\033[1;31m\n\n\nDo you wish to
    
        1) Go to main menu
        2) Exit
    
Pick one: \033[0;37m'''))
        
    except (ValueError, TypeError):
        print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
        time.sleep(2)
        Fetch_Novel_Desc(Fetch_Link)
    else:
        if int(Fetch_Novel_Desc.Choice)==1:
            print("\n\n\n")
            Listing()    
        elif int(Fetch_Novel_Desc.Choice)==2:
            exit()
        else:
            print("\033[1;31m\nInvalid Choice. Please pick again.\n\n\n\033[0;37m")
            time.sleep(2)
            Fetch_Novel_Desc(Fetch_Link)

#Function to check and change whether an element is a String or a Tag, if it is a tag with <br> or <br> extract the data and check again, return the list after appending all the extracted strings in it.
def Change(Element):
    if str(type(Element))=="<class 'bs4.element.NavigableString'>":
        if "<br>" in Element:
            Element=Element.replace("<br>","")
        elif "</br>" in Element:
            Element=Element.replace("</br>","")
        Status.append(Element)
        if "\n" in Status:
            Status.remove("\n")
    elif str(type(Element))=="<class 'bs4.element.Tag'>":
        for Extract in Element:
            Change(Extract)
    return(Status)

Start()
