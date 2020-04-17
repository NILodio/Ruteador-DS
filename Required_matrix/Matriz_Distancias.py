import pandas as pd  # linear algebra
import numpy as np  # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
import json
import urllib.request




def create_distance_matrix(data):
    addresses_Latitud = list(data['Latitud'].values())
    addresses_Longitud = list(data['Longitud'].values())
    Clients = data['Nombre del cliente']
    API_key = data['API_key'] # Api To get Data From Google
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(Clients)
    #print(num_addresses)
    max_rows = max_elements // num_addresses
    #print(max_rows)
    q , r = divmod(num_addresses,max_rows)
    #print(q,r)
    dest_addresses_Latitud = addresses_Latitud
    dest_addresses_Logitud = addresses_Longitud
    distance_matrix = []
    # Send q requests , returning max_rows per request

    for i in range(q):
    #print(addresses_Latitud[])
        origin_address_Latitud = addresses_Latitud[i * max_rows: (i+1) * max_rows]
        origin_address_Longitud = addresses_Longitud[i * max_rows: (i+1) * max_rows]
        response = send_request(origin_address_Latitud,origin_address_Longitud,dest_addresses_Latitud,dest_addresses_Logitud, API_key)
        distance_matrix += build_distance_matrix(response)
    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_address_Latitud = addresses_Latitud[q * max_rows:q *max_rows + r]
        origin_address_Longitud = addresses_Longitud[q * max_rows:q *max_rows + r]
        response = send_request(origin_address_Latitud,origin_address_Longitud,dest_addresses_Latitud,dest_addresses_Logitud, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix



def send_request(origin_address_Latitud,origin_address_Longitud,dest_addresses_Latitud,dest_addresses_Logitud, API_key):
    
  """ Build and send request for the given origin Latitud an longitd."""
  def build_Longitud_Latitud_str(addresses_Latitud,addresses_Longitud):
    # Build a pipe-separated string of send
    str_send = ''
    for i in range(len(addresses_Latitud) - 1):
      str_send += str(addresses_Latitud[i]) +","+ str(addresses_Longitud[i])  + '|'
    str_send += str(addresses_Latitud[-1]) +","+ str(addresses_Longitud[-1])
    return str_send

  request_data = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_Longitud_Latitud_str(origin_address_Latitud,origin_address_Longitud)
  dest_address_str = build_Longitud_Latitud_str(dest_addresses_Latitud,dest_addresses_Logitud)
  request_data = request_data + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  #print(request_data)
  with urllib.request.urlopen(request_data) as url:
      jsonResult = url.read()

  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix



def crate_data():
    df = pd.read_csv('test.csv',encoding="ISO-8859-1")
    df = df.to_dict()
    df['API_key'] = 'AIzaSyAR-Rf9ctFqLTHePDs3oUCuz3g4CGwYTh4'
    #print(type(df))
    return df

########
# Main #

########

def main():
    """Entry point of the program"""
    data = crate_data()
    #addresses = data['Direcci¢n']
    #print(data)
    #API_key = ""
    distance_matrix = create_distance_matrix(data)
    df = pd.DataFrame(distance_matrix)
    df.to_csv('Sample_P.csv',index=False)

    

if __name__ == '__main__':
  main()
