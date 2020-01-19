import urllib.request

import json

def get_time_estimation(home_location, work_location):
       key = 'AIzaSyDR70J4nTVbHVfCx6Cm9Jbd93hIh2zI2bg'
       traffic_model = "pessimistic"
       mode ="driving"
       departure_time = "now"
       url = ('https://maps.googleapis.com/maps/api/distancematrix/json'

              + '?language=en-US&units=imperial'

              + '&origins={}'

              + '&destinations={}'

              + '&key={}'

              + '&mode={}'

              + '&traffic_model={}'

              + '&departure_time={}'
              ).format(home_location.replace(' ','+'), work_location.replace(' ','+'), key,mode,traffic_model,departure_time)


       response = urllib.request.urlopen(url)

       response_json = json.loads(response.read())
       # distance_meters = response_json['rows'][0]['elements'][0]['distance']['text']

       distance_minutes = response_json['rows'][0]['elements'][0]['duration']['text'] 
       return distance_minutes

       # print("Travel time to "+destination.replace('+',' ')+" is "+distance_minutes)
       # print("by "+mode)
       # print("tm "+traffic_model)

# origin = input("from ").replace(' ','+')

# destination = input("to ").replace(' ','+')

# key = 'AIzaSyDR70J4nTVbHVfCx6Cm9Jbd93hIh2zI2bg'
# traffic_model = "pessimistic"
# mode ="driving"
# departure_time = "now"
# url = ('https://maps.googleapis.com/maps/api/distancematrix/json'

#        + '?language=en-US&units=imperial'

#        + '&origins={}'

#        + '&destinations={}'

#        + '&key={}'

#        + '&mode={}'

#        + '&traffic_model={}'

#        + '&departure_time={}'
#        ).format(origin, destination, key,mode,traffic_model,departure_time)


# response = urllib.request.urlopen(url)

# response_json = json.loads(response.read())
# distance_meters = response_json['rows'][0]['elements'][0]['distance']['text']

# distance_minutes = response_json['rows'][0]['elements'][0]['duration']['text'] 


# print("Travel time to "+destination.replace('+',' ')+" is "+distance_minutes)
# print("by "+mode)
# print("tm "+traffic_model)