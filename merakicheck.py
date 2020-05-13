from webexteamssdk import WebexTeamsAPI
import requests
meraki_api_key = '093b24e85df15a3e66f1fc359f4c48493eaa1b73'
mynetwork = 'L_646829496481100388'

msversion = '11.31'
mrversion = '26.6.1'
mxversion = '15.27'
mvversion = '4.0'
WebexRoomID = "Y2lzY29zcGFyazovL3VzL1JPT00vNWJiMmRiZjAtNmFkOC0xMWVhLWEzNmEtMDc0ZjMxN2Y0Njli"
myWebexToken = "" #you will need to put your personal token here

switch_firmware = f"switch-{msversion.replace('.','-')}"
ap_firmware = f"wireless-{mrversion.replace('.','-')}"
sec_appliance_firmware = f"wired-{mxversion.replace('.','-')}"
camera_firmware = f"camera-{mvversion.replace('.','-')}"

baseurl = "https://dashboard.meraki.com/api/v0/networks/"

payload = {}
headers = {'X-Cisco-Meraki-API-Key': '093b24e85df15a3e66f1fc359f4c48493eaa1b73'} #you will need to look to the meraki_api_key

url = baseurl + mynetwork + '/devices' #finish the url!

response = requests.get(url, headers=headers, data=payload) #complete the api call using the requests library

myresponse = response.json()

compliant_switches = 0
compliant_aps = 0
compliant_sec_appliances = 0
compliant_cameras = 0
non_compliant_devices = []

for device in myresponse:
    if device['firmware'] == switch_firmware:
        compliant_switches += 1
    elif device['firmware'] == ap_firmware:
        compliant_aps += 1
    elif device['firmware'] == sec_appliance_firmware:
        compliant_sec_appliances += 1
    elif device['firmware'] == camera_firmware:
        compliant_cameras += 1
    else:
        non_compliant_devices.append(device)

print(f'Total switches that meet the standard: {compliant_switches}')
print(f'Total APs that meet the standard: {compliant_aps}')
print(f'Total Security Appliances that meet the standard: {compliant_sec_appliances}')
print(f'Total Cameras that meet the standard: {compliant_cameras}')
print('Devices that will need to be manually checked:')

for device in non_compliant_devices:
    print(f"Serial#: {device['serial']}, Model#: {device['model']}")

#Post message to Teams
teams_api = WebexTeamsAPI(access_token=myWebexToken)
teams_api.messages.create(roomId=WebexRoomID, text='Report Completed')
