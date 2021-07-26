import requests




class REQUESTX:

    def transmit(self, freq, status):
        
        msg = {"STATUS":status,"FREQ":freq}
        #print(msg)
        try : 
            r = requests.post('http://10.8.2.15/atualiza/freq', json=msg)
            r.status_code
        return r.text
        except:
            return "error"


#print (REQUESTX().transmit(145.4,"OFF"))