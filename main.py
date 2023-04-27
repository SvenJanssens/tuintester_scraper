from bs4 import BeautifulSoup
import requests
import re
import tomllib

with open("config.toml", "rb") as f:
    login = tomllib.load("login")
    password = tomllib.load("password")
    dashboard_days = tomllib.load("dashboard_days")


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

data = {'user[email]': login,
        'user[password]': password,
        'user[remember_me]': "0",
        'commit': 'Login'}

with requests.session() as sess:
    post_data = sess.get('https://dashboard.wetlands4cities.be/users/sign_in')
    html = BeautifulSoup(post_data.text, 'html.parser')
    
    #Update data
    data.update(authenticity_token= html.find("input", {'name':'authenticity_token'}).get('value'))
    #Login
    res = sess.post("https://dashboard.wetlands4cities.be/users/sign_in", data=data, headers=headers)
    
    #Check login
    res = sess.get('https://dashboard.wetlands4cities.be/dashboard?days=' + dashboard_days)

    soup = BeautifulSoup(res.text, 'html.parser')  

    try:
        script = soup.find_all('script', string=re.compile("window.chart_data"))
    except:
        print ('Your username or password is incorrect')
    else:
        print ("You have successfully logged in as", login)
        script = str(script[0])
        begin = script.find("window.chart_data") + 20
        end = script.find("} ;") + 1
        chart_data = script[begin:end]
        # chart_data contains the following data series:
        #   - t1 : soil temperature
        #   - t2 : surface temperature
        #   - t3 : air temperature
        #   - humidity : soil humidity
        #
        # Depending on for how many days the dashboard needs to show data points the time interval changes. 
        # F.e.: If you request data for 7 days, then you get data points for every hour. 
        # This interval increases to 4 hours for longer periods.
        # { 
        #   "<serie>": [
        #       {
        #           "x":<date string formatted as yyyy-mm-dd HH:MM:SS>
        #           "y":<float value>
        #       },
        #       ...
        #   ],
        #   ...
        # }

        begin = script.find("window.temperaturs") + 21
        end = script.find("} ;", begin) + 1
        temperaturs = script[begin:end]
        # temperaturs contains the following derived data:
        #   {
        #       "min_t1":<float>,
        #       "max_t1":<float>,
        #       "mean_t1":<float>,
        #       "min_t2":<float>,
        #       "max_t2":<float>,
        #       "mean_t2":<float>,
        #       "min_t3":<float>,
        #       "max_t3":<float>,
        #       "mean_t3":<float>
        #   }
        print("Chart Data:", chart_data)
        print("Derived:", temperaturs)