import requests, json,os, csv

Serial_B3='CNNSKD5D5K'
#customer_id= 'i0ZNS6wXGAcJPpkU9EveTj6OEZgJSX9r'
#myToken = 'S1q4AM347gKJH2zMGtVFaqPBxoPzKljW'
client_id="LTmroqUaoK75QX6ymdIjTLE1wmBHVvLa"
client_secret="c46b643GxnhwofW0gn0xCicUDXBDM8Zo"
access_token=""
refresh_token=""

def RefreshToken():

    Payload = '{  "client_id" : "' + client_id + '", "client_secret": "' + client_secret + '" , "grant_type" : "refresh_token" , "refresh_token" : "' + refresh_token + '" }'
    #print (Payload)
    x=json.loads(Payload)

    myUrl = 'https://apigw-uswest4.central.arubanetworks.com/oauth2/token'
    response = requests.post(myUrl, json=x)
    print (response.content)
    with open("token.json", "w") as outfile:
        outfile.write(response.text)
      
    

def Cambia_Nombre(AP_SerialNumber,AP_HostName):
    
    Payload = '{"hostname": "Old_Hostname","ip_address": "0.0.0.0", "zonename": "_#ALL#_","achannel": "0", "atxpower": "-127","gchannel": "0","gtxpower": "-127","dot11a_radio_disable": false,"dot11g_radio_disable": false,   "usb_port_disable": false}'
    Payload =Payload.replace('Old_Hostname',AP_HostName)
    #print (Payload)
    x=json.loads(Payload)
    #print (json.dumps(x, indent=4))

    myUrl = 'https://apigw-uswest4.central.arubanetworks.com/configuration/v2/ap_settings/' + AP_SerialNumber
    #print (access_token)
    head = {'Authorization': 'token {}'.format(access_token)}
    #print(myUrl)
    #print(head)
    #response = requests.get(myUrl, headers=head)
    response = requests.post(myUrl, headers=head, json=x)
    print (response.status_code)
    if response.status_code==200:
        print ('Nombre Cambiado\n\n')
    else:
        print ('Error: ')
        print (response.status_code)
    

    #response = requests.get(myUrl, headers=head)
    #response = requests.post(myUrl, headers=head, json=payload)
    #print (response.content)

def Cambia_Grupo(AP_SerialNumber,AP_Group):
    
    Payload = '{  "group" : "' + AP_Group + '", "serials": [   "' + AP_SerialNumber + '"  ]}'
    x=json.loads(Payload)
    #print (json.dumps(x, indent=4))
    myUrl = 'https://apigw-uswest4.central.arubanetworks.com/configuration/v1/devices/move'
    head = {'Authorization': 'token {}'.format(access_token)}
    response = requests.post(myUrl, headers=head, json=x)
    print (response.content)
    if response.status_code==200:
        
        print ('\tGrupo Actualizado\n\n')
    else:
        print ('Error: ')
        print (response.status_code)

def Cambia_Sede(AP_SerialNumber,AP_Sede): 

    Payload = '{ "device_id": "' + AP_SerialNumber + '","device_type": "IAP","site_id": ' + AP_Sede + '}'
    x=json.loads(Payload)
    print (json.dumps(x, indent=4))
    myUrl = 'https://apigw-uswest4.central.arubanetworks.com/central/v2/sites/associate'
    head = {'Authorization': 'token {}'.format(access_token)}
    response = requests.post(myUrl, headers=head, json=x)
    print (response.content)
    if response.status_code==200:
        
        print ('\tSede Actualizada\n\n')
    else:
        print ('Error: ')
        print (response.status_code)

def ReadToken():
    global access_token, refresh_token

    # Opening JSON file
    with open('./src/token.json', 'r') as openfile:
 
        # Reading from json file
        token = json.load(openfile)
 
    access_token=token["access_token"]
    refresh_token=token["refresh_token"]

def ListarSedes():
        #   Script para Listar Sedes
        myUrl = 'https://apigw-uswest4.central.arubanetworks.com/central/v2/sites'
        head = {'Authorization': 'token {}'.format(access_token)}
        response = requests.get(myUrl, headers=head)
        print (response.status_code)
        json_txt= response.text
        with open("sedes.json", "w") as outfile:
            outfile.write(response.text)
        y=json.loads(json_txt)
        #print (json.dumps(y, indent=4))
        with open("sedes.csv", "w") as outfile:
            for  row in y["sites"]:
                outfile.write (str(row["site_id"]) +" , "+ row["site_name"] + "\n")

# Clearing the Screen
os.system('clear')


# myUrl = 'https://apigw-uswest4.central.arubanetworks.com/msp_api/v1/customers/0b613ed0c9f311ed9b8e5a6f0e07d928/devices?limit=100&device_type=iap'
head = {'Authorization': 'token {}'.format(access_token)}
#response = requests.get(myUrl, headers=head)

ReadToken()


print("Menú:\n")
print("1.- Cambia Nombre")
print("2.- Cambia Grupo")
print("3.- Cambia Sede")
print("4.- Listar Sedes")
print("5.- Refresh Token")
print("6.- Salir")
option = input("Ingrese una opción:")

match option:
    case "1":
        #   Script para Cambiar Nombre de AP
        with open('AP_List.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print('+ '.join(row))
                print ('Cambiando Nombre del AP SN:'+ row[0]+ ' a ' + row[1] +'\n')
                Cambia_Nombre(row[0],row[1])
    case "2":
        #   Script para Cambiar Grupo de AP
        with open('AP_List.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print('+ '.join(row))
                print ('Cambiando el Grupo del AP SN:'+ row[0]+ ' a ' + row[2] +'\n')    
                Cambia_Grupo(row[0],row[2])
    case "3":
        #   Script para Cambiar Sede de AP
        with open('AP_List.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print('+ '.join(row))
                print ('Cambiando la Sede Grupo del AP SN:'+ row[0]+ ' a ' + row[3] +'\n')    
                Cambia_Sede(row[0],row[3])
    case "4":
        ListarSedes()

    case "5":
        RefreshToken()

    case "6":
        print("\nBye Bye\n")

"""
Desasociar un AP de un Sitio
Delete
/central/v2/sites/associate

{
  "device_id": "CNPJLBN7N7",
  "device_type": "IAP",
  "site_id": 4
}

Asociar un AP a un sitio
Post
/central/v2/sites/associate
{
  "device_id": "AD12412345",
  "device_type": "IAP",
  "site_id": 4
}

"""