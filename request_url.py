import requests
from time import sleep



class REQUESTX:

    def transmit(self, freq, status):

        if freq > 300:
            url = "10.8.2.16"
        else :
            url = "10.8.2.16"

        Loop = True
        urlTX = f'http://{url}/atualiza/freq'
        msg = {'STATUS':f'{status}','FREQ':f'{freq}'}
        print(urlTX)
        while Loop:
            try : 
                print(msg)
                r = requests.post(urlTX, json=msg)
                r.status_code
                print(r.status_code)
                print(r.text)
                if r.status_code == 200:
                    Loop = False
            except:
                pass
            sleep(0.2)
        return r.text


#print (REQUESTX().transmit(400.0,"OFF"))
