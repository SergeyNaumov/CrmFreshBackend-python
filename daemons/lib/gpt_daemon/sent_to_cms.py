import requests

def sent_to_cms(BackendBase:  str, obj:dict):
    #print('BaсkendBase:',BaсkendBase)
    #quit()
	url = f"{BackendBase}/gpt-assist/daemon-result"

	#requests.post(url,  )
	print('url: ',url)
	print('obj:',obj)
	resp = requests.post(url, json=obj)
	print('resp: ',resp)