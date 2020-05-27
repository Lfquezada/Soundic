import urllib.request
import urllib.parse
import re
import webbrowser as wb


#funcion para abrir link en youtube
def PlaySong(artist, song):
    #Song and artist for search
    query = str(artist) +" "+ str(song)
    #encode to URL
    query_string = urllib.parse.urlencode({"search_query" : query})
    #Search in YouTube
    html_content = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
    #List of results
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    #show final URL
    print("http://www.youtube.com/watch?v=" + search_results[0])
    #Open URL in Web Browser
    wb.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))

