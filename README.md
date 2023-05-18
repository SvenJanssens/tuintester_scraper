# tuintester_scraper

Participating with the Belgian Tuintester project (part of the European wide program Wetlands4Cities - more info here: https://www.mechelen.be/tuintesters), I wanted to extract the data shown on the website https://dashboard.wetlands4cities.be/dashboard and log it locally.

There is no API provided, so it was necessary to write a scraper to access this data.

The data is only uploaded from the sensor to the dashboard around midnight, so it doesn't make sense to run the scraper more than once a day.

The code results in the variables chart_data and temperaturs containing a JSON string with the extracted data.

## chart_data
chart_data contains the following data series:
- t1 : soil temperature
- t2 : surface temperature
- t3 : air temperature
- humidity : soil humidity

Depending on for how many days the dashboard needs to show data points the time interval changes.<br/>
F.e.: If you request data for 7 or 30 days, then you get data points for every 15 minutes. <br/>
If you request data for 90, 365 days or everything, then you get data points for every 4 hours.<br/>
{ <br/>
  "serie": [ <br/>
    {<br/>
      "x":date string formatted as yyyy-mm-dd HH:MM:SS><br/>
      "y":float value<br/>
    },<br/>
    ...<br/>
  ],<br/>
  ...<br/>
}<br/>

## config.toml
To make it run, you will need to add a config.toml file to the project. It should contain the following lines:<br/>
login = "email used to logon to the dashboard"<br/>
password = "meter id for which you want the data"<br/>
dashboard_days = "how many days you want data for"<br/>
