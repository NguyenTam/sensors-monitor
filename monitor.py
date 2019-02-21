# for http get and post
import requests

# for plotting
import matplotlib.pyplot as plt

# for detecting environment and taking screenshot 
import os

# for printing error date and time.
import datetime

# for delaying
import time

# Constants
DATE = "date"
SENSOR1 = "sensor1"
SENSOR2 = "sensor2"
SENSOR3 = "sensor3"
SENSOR4 = "sensor4"
SAMPLE_SIZE_LIMIT = 7

EMAIL = "ccc@hotmail.com"
PASSWORD = "anypassword"

def signup(email, password):
    """
    Register.
    
    Parameters
    ----------
    email : str
    password : str
    
    Returns
    ----------
    int : status code
    """
    r = requests.post(r"https://opendata.hopefully.works/api/signup", json={"email":email, "password":password})
    
    return r.status_code

def getToken(email, password):
    """
    This function return an access token retrieved from api/login
    
    Parameters
    ----------
    email : str
    password : str
    
    Returns
    ----------
    access token
        if access token is retrieved. 
    empty string
        Otherwise.
    """
    r = requests.post(r"https://opendata.hopefully.works/api/login", json={"email":email, "password":password})
    if r.status_code == 200:    
        return r.json()["accessToken"]
    else:
        return ""
    
def getJsonData(accessToken):
    """
    Parameters
    ----------
    accessToken : str
        an access token to access api/events
    
    Returns
    ----------
    json : dict
        An empty json data if could not retrieve an event. Otherwise json data containing four sensors data and date.
    """
    r = requests.get(r"https://opendata.hopefully.works/api/events", headers={'Authorization': 'Bearer {}'.format(accessToken)})
    if r.status_code == 200:
        return r.json()
    else:
        return {}

def initializeCollection():
    """
    Initialize a collection to be plotted.
    
    Returns
    ----------
    dictionary
        keys and their initial values.
    """
    return {SENSOR1:[], SENSOR2:[], SENSOR3:[],SENSOR4:[], DATE:[]}


def appendJsonData(jsondata, destination):
    """
    Append jsondata to destination, a collection to be plotted
    
    Parameters
    ----------
    jsondata : dict
        a data to be appended.
    destination : dict
        a collection of data.
    """
    for k,v in jsondata.items():
        destination[k].append(v)
        
def plot(accessToken, collection):
    """
    Retrieve json data and plot the collection of json data.
    
    Parameters
    ----------
    accessToken : str
        an access token to access api/events
    collection : dict
        append json data to this collection and plot it.
    """
    
    plt.xlabel('Date/Time')
    plt.ylabel('Sensor Value')
    plt.title("Sensors Monitor")
    
    # to save png files
    i = 0
    
    # set interactive mode on
    plt.ion()
    
    # set figure to full screen
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    while True:
        jsondata = getJsonData(accessToken)
        if jsondata:
            #limit date string
            jsondata[DATE] = jsondata[DATE][8:13]
            appendJsonData(jsondata, collection)
            
            # clear figure
            plt.clf()
            
            # limit samples to be viewed
            if (len(collection[DATE]) > SAMPLE_SIZE_LIMIT):
                plt.xticks(range(SAMPLE_SIZE_LIMIT), collection[DATE][-SAMPLE_SIZE_LIMIT:])
                plt.plot(collection[SENSOR1][-SAMPLE_SIZE_LIMIT:], 'k', label='sensor 1')
                plt.plot(collection[SENSOR2][-SAMPLE_SIZE_LIMIT:], 'b', label='sensor 2')
                plt.plot(collection[SENSOR3][-SAMPLE_SIZE_LIMIT:], 'g', label='sensor 3')
                plt.plot(collection[SENSOR4][-SAMPLE_SIZE_LIMIT:], 'r', label='sensor 4')
            else:
                plt.xticks(range(len(collection[DATE])), collection[DATE])
                plt.plot(collection[SENSOR1], 'k', label='sensor 1')
                plt.plot(collection[SENSOR2], 'b', label='sensor 2')
                plt.plot(collection[SENSOR3], 'g', label='sensor 3')
                plt.plot(collection[SENSOR4], 'r', label='sensor 4')
                
            plt.legend(loc='upper left')
            plt.show()
            
            # Take a screenshot on Gnome desktop
            if os.environ.get("XDG_MENU_PREFIX").startswith("gnome"):
                os.system("gnome-screenshot -f screenshot{}.png".format(i))
                i = i+1
                            
            #plt.pause(1)
            plt.pause(60*60) # one hour
        else:
            print(str(datetime.datetime.now()) + " Empty json data")
        
def main():
    collection = initializeCollection()
    
    signupStatus = signup(EMAIL, PASSWORD)
    
    # 201 = created
    if signupStatus == 201:
        print("Registered successfully")
    else:
        print("Could not register")
    
    accessToken = getToken(EMAIL, PASSWORD)
    if accessToken:
        print("Plotting....")
        plot(accessToken, collection)
    else:
        print("Could not retrieve an access token")
        
main()