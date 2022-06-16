# Description:
# Use the weather API to retrieve the current day's forecast and print out the forecast.

import requests
import json

def printWelcome():
    print("Hi there! Welcome to free weather reports with no ads! \nOnce you're done inputting the cities, type 'end' to retrieve weather forecasts.")
    print("---")


# function to properly format city name
def formatCity(cityname):
    cityname = cityname.lower()
    cityCap = list(cityname)
    cityCap[0] = cityCap[0].upper()
    for i in range(len(cityCap)):
        if cityCap[i] == " ":
            cityCap[i + 1] = cityCap[i + 1].upper()
    cityname = "".join(cityCap)
    return cityname


# function to take in city input and save by appending to list to check if city was saved
def saveCity(cityList, apiKey):
    city = input("Input city for weather data: ")
    city = city.lower()
    while city != "end":
        city = formatCity(city)
        if city in cityList:  # if the city is already entered
            print("Sorry, that city is already entered!")
        else:  # if the city has not been entered
            if callAPI(city, apiKey):  # if is valid city
                cityList.append(city)
                print("Saved, data retrieved!")
            else:  # if city is not vali
                print("Not saved, bad city request!")
        city = input("Input weather data: ")
        city = city.lower()
    print("---")
    return cityList


# # function to call API and see if city is valid
def callAPI(cityName, apiKey):
    # pass in city to get info from by q="city name"
    response = requests.get("http://api.weatherapi.com/v1/current.json?key=" + apiKey + "&q=" + cityName + "&aqi=yes")
    # apiCityName = response.json()["location"]["name"]
    # print(apiCityName)
    if response.status_code != 200:
        return False
    elif response.json()["location"]["name"] != cityName:
        return False
    else:
        return True


# function to get weather and return a list of all the forecast info
def getForecast(cityList, apiKey):
    city = input("For what city would you like weather information? ")
    city = city.lower()
    while city != "exit":
        forecastList = []
        if city == "all":
            for i in range(len(cityList)):
                forecastList = []
                print("I do have information about the weather in " + cityList[i] + ":")
                response = requests.get(
                    "http://api.weatherapi.com/v1/forecast.json?key=" + apiKey + "&q=" + cityList[i] + "&days=1&aqi=no&alerts=no")
                forecast = response.json()['forecast']
                forecastday = forecast["forecastday"]
                day = forecastday[0]["day"]
                highTemp = day["maxtemp_f"]
                minTemp = day["mintemp_f"]
                humidity = day["avghumidity"]
                windSpeed = day["maxwind_mph"]
                rainChance = day["daily_chance_of_rain"]
                snowChance = day["daily_chance_of_snow"]
                condition = day['condition']['text']
                forecastList.extend([highTemp, minTemp, humidity, windSpeed, rainChance, snowChance, condition])
                printForecast(forecastList)
                print("")
        else:
            city = formatCity(city)
            if city in cityList:
                print("I do have information about the weather in " + city + ":")
                response = requests.get(
                    "http://api.weatherapi.com/v1/forecast.json?key=" + apiKey + "&q=" + city + "&days=1&aqi=no&alerts=no")
                forecast = response.json()['forecast']
                forecastday = forecast["forecastday"]
                day = forecastday[0]["day"]
                highTemp = day["maxtemp_f"]
                minTemp = day["mintemp_f"]
                humidity = day["avghumidity"]
                windSpeed = day["maxwind_mph"]
                rainChance = day["daily_chance_of_rain"]
                snowChance = day["daily_chance_of_snow"]
                condition = day['condition']['text']
                forecastList.extend([highTemp, minTemp, humidity, windSpeed, rainChance, snowChance, condition])
                printForecast(forecastList)
            else:  # city is not in saved
                print("I do not have information about the weather in " + city + ".")
            print("---")
        city = input("For what city would you like weather information? ")
        city = city.lower()
    print("Goodbye!")


# print out the weather forecast
def printForecast(forecastList):
    print("The high temperature is", forecastList[0], "degrees Fahrenheit.")
    print("The low temperature is", forecastList[1], "degrees Fahrenheit.")
    print("The humidity is " + str(forecastList[2]) + "%.")
    print("The wind speed is", forecastList[3], "mph.")
    precipitation = float(precipitationCal(forecastList[4], forecastList[5]))
    format_precip = '{0:.1f}'.format(precipitation)  # convert precipitation to 1 decimal place
    print("The chance of precipitation is " + format_precip + "%.")
    print(forecastList[6] + ".")


# calculate the precipitation and return the max of the 2 values
def precipitationCal(dailyRain, dailySnow):
    return max(dailyRain, dailySnow)


def main():
    apiKey = "24b5c0a38b084ea2ac8185000220504"
    cityList = []
    printWelcome()
    saveCity(cityList, apiKey)
    getForecast(cityList, apiKey)

main()