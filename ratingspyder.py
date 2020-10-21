import requests
from bs4 import BeautifulSoup
import imdb

def get_page(url):
    response= requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    

    if not response.ok:
        print("Server status ",response.status_code)
    else:
        soup=BeautifulSoup(response.text,'lxml')
    return soup

def get_rottentomatoes(name):
    try:
        print("--Rotten tomatoes--")
        name=name.replace(' ','-')
        url="https://www.rottentomatoes.com/tv/"+name
        soup=get_page(url)
        rating=soup.find('span', class_='mop-ratings-wrap__percentage')
        try:
            title=soup.find('h1', class_='title')
            title=str(title.text)
            check = " ".join(title.split())
            print(check)
        except Exception as e:
            print("Title tag not found")

        percentage=(rating.text).replace(" ", "").replace("\t", "")
        rating=(float(percentage[1:3]))/10
        print("Rating:"+str(rating))
    except Exception:
        print("Couldn't scrape rating")
        return 0
    return rating

def get_imdb(name):
    moviesDB = imdb.IMDb()
    movies = moviesDB.search_movie(name)
    movie=movies[0]
    print("--IMDB--")
    print(str(movie['title']) +" "+ str(movie['year']))
    id=movies[0].getID()
    info=moviesDB.get_movie(id)
    print("Rating:"+str(info['rating']))
    return float(info['rating'])

def get_meta(name):
    try:
        print("--Metacritic--")
        name=name.replace(' ','-')
        url="https://www.metacritic.com/tv/"+name
        soup=get_page(url)
        rating = soup.find('div', class_='metascore_w user larger tvshow positive')
        try:
            title=soup.find('div', class_='product_page_title oswald').find('h1')
            date=soup.find('span', class_='release_date')
            date=(date.text).split(':')[1]
            date= " ".join(date.split())
            title=str(title.text)
            check = " ".join(title.split())
            print(check+" "+str(date))
        except Exception as e:
            print("Title tag not found")
        print("Rating:" + str(rating.text))
    except Exception:
        print("Couldn't scrape rating")
        return 0
    return float(rating.text)




def main():
    name=input("Enter Name(without caps):")
    rotten=get_rottentomatoes(name)
    #print(rotten)
    meta=get_meta(name)
    imdb=get_imdb(name)
    if(rotten==0 and meta==0):
        avg=imdb
    elif (rotten==0 or meta==0):
        avg=(rotten+meta+imdb)/2
    else:
        avg=(rotten+meta+imdb)/3
    print("\n\nAVERAGE:",avg)
if __name__=='__main__':
    main()
