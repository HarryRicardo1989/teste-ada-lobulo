#!/bin/python3

import address_commands as ac
from tcp_socket import TcpSocket
from ada_control import AdaControl
from gqrx_control import RemoteControl
from time import sleep


class TesteAda:
    def __init__(self):
        self.gqrx_ctr = RemoteControl(*ac.gqrx_addr_port)
        self.ada_ctr = AdaControl()
        self.signal_power = 0.0
        self.freq = 145
        #self.NomeArquivo = "intensidade_QCDup"
        pass

    def ada_teste(self, pos_az_init, pos_az_end, pos_el, media_num, frequencia,timer,TX_power): #,NomeArquivo="intensidade_QCDup"):
        self.freq = frequencia
#        self.NomeArquivo = NomeArquivo
        self.tempo_espera = timer
        self.TX_power = TX_power
        self.pos_el = pos_el

        for pos_az in range(int(pos_az_init), int(pos_az_end)+1, 1):
            position = False
            print(f'Azimute = {pos_az} graus. Elevacao {self.pos_el}')
            self.ada_ctr.set_ada_pos(float(pos_az), self.pos_el)
            sleep(self.tempo_espera)
            self.grava_resultado(pos_az, self.gqrx(media_num))
        print('finalizado')

    def gqrx(self, media_num):
        self.gqrx_ctr.set_controls(ac.set_freq, f'{self.freq}e6')
        sleep(0.1)
        self.gqrx_ctr.get_status(ac.signal_power)
        self.gqrx_ctr.get_status(ac.signal_power)
        self.gqrx_ctr.get_status(ac.signal_power)
        self.gqrx_ctr.get_status(ac.signal_power)
        sleep(0.3)
        signal_list = []
        signal_power = 0
        for teste in range(0, media_num):
            signal_power = float(self.gqrx_ctr.get_status(ac.signal_power))
            signal_list.append(signal_power)
            print(f'{teste+1} Signal Power {signal_power} dBFS')
            sleep(0.5)
        return round(sum(signal_list) / len(signal_list),2)

    def grava_resultado(self, pos, signal_power):
        with open(f'./teste-ADA-IntensidadeQCDup.csv', 'a') as file:
            file.write(f'TX = {self.TX_power}dBm |Azimute = {pos}|Elevacao = {self.pos_el}|{signal_power} dBFS \n')


if __name__ == '__main__':
    
    print("Inicio Teste Lobulo de irradiacao: ")
    
#    pos_az_init = float(input("Digite a posicao de azimute inicial: "))

#    pos_az_end = float(input("Digite a posicao de azimute final: "))

#    pos_el = float(input("Digite a posiçao de elevacao: "))

#    media_num = int(input("Digite a quantidade de coletas para media: "))

    frequencia = float(input("Digite frequencia desejada: "))

#    timer = int(input("Digite tempode espera entre coletas: "))

#    TX_power = float(input("Digite potencia de transmicao do sinal em dBm: "))
    
#    NomeArquivo = str(input("Digite o Sufixo do arquivo: "))  

    print("Inicio Teste Lobulo de irradiacao: ")

#    TesteAda().ada_teste(pos_az_init, pos_az_end, pos_el, media_num, frequencia,timer,TX_power,NomeArquivo)
    TesteAda().ada_teste(6.00, 6.00, 0.00, 20, frequencia, 5, -40)
