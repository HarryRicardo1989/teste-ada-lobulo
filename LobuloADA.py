#!/bin/python3
from request_url import REQUESTX
import address_commands as ac
from tcp_socket import TcpSocket
from ada_control import AdaControl
from gqrx_control import RemoteControl
from time import sleep


class TesteAda:
    def __init__(self):
        self.gqrx_ctr = RemoteControl(*ac.gqrx_addr_port)
        self.URL = REQUESTX()
        self.ada_ctr = AdaControl()
        self.signal_power = 0.0
        pass

    def ada_teste(self, pos_az_init, pos_az_end, pos_el_init, pos_el_end, media_num, frequencia_init, frequencia_end, timer, NomeArquivo, incremento):
        self.pos_az_init = pos_az_init
        self.pos_az_end = pos_az_end
        self.pos_el_init = pos_el_init
        self.pos_el_end = pos_el_end
        self.media_num = media_num
        self.frequencia_init = int(frequencia_init * 10)
        self.frequencia_end =  int(frequencia_end *10)
        self.tempo_espera = timer
        self.NomeArquivo = NomeArquivo
        self.URL.transmit(frequencia_init, "ON")
        self.incremento = int(incremento *10)


        for freq in range(int(self.frequencia_init), int(self.frequencia_end)+1, self.incremento):
            #print(freq, self.frequencia_init, self.frequencia_end)
            frequencia = freq /10
            self.ada_ctr.set_ada_pos(float(self.pos_az_init), float(self.pos_el_init))
            self.gqrx_ctr.set_controls(ac.set_freq, f'{frequencia}e6')
            self.URL.transmit(frequencia, "ON")
            sleep(self.tempo_espera)
            for pos_el in range(int(self.pos_el_init), int(self.pos_el_end)+1, 1):
                for pos_az in range(int(self.pos_az_init), int(self.pos_az_end)+1, 1):
                    print(
                        f'Azimute = {pos_az} graus. Elevacao {pos_el} freq {frequencia}')
                    self.ada_ctr.set_ada_pos(float(pos_az), pos_el)
                    sleep(self.tempo_espera)
                    
                    self.grava_resultado(
                        pos_az, pos_el, frequencia, self.gqrx(media_num))
        print('finalizado')
        self.URL.transmit(140, "OFF")

    def gqrx(self, media_num):
        signal_power = 0
        signal_list = []
        for teste in range(0, media_num):
            signal_power = float(self.gqrx_ctr.get_status(ac.signal_power))
            signal_list.append(signal_power)
            print(f'{teste+1} Signal Power {signal_power} dBFS')
            sleep(0.2)
        return round(sum(signal_list) / len(signal_list),2)

    def grava_resultado(self, pos_az, pos_el, freq, signal_power):
        with open(f'/var/log/Resultados/{self.NomeArquivo}.csv', 'a') as file:
            file.write(
                f'Frequencia = {freq} MHz |Azimute = {pos_az}|Elevacao = {pos_el}|{signal_power} dBFS \n')

    def Inicio(self):

        pos_az_init = float(input("Digite a posicao de azimute Inicial: "))
        pos_az_end = float(input("Digite a posicao de azimute Final: "))
        pos_el_init = float(input("Digite a posiçao de elevacao Inicial: "))
        pos_el_end = float(input("Digite a posiçao de elevacao Final: "))
        frequencia_init = float(input("Digite frequencia Inicial desejada: "))
        frequencia_end = float(input("Digite frequencia Final desejada: "))
        incremento = float(input("Digite o incremento de frequencia em MHz: "))
        media_num = int(input("Digite a quantidade de coletas para media: "))
        timer = int(input("Digite tempo de espera entre coletas: "))
        NomeArquivo = str(input("Digite o Nome do arquivo: "))
        voltas = int(input("Digite a quantidade de vezes que o teste será executado: "))

        quantAZ = pos_az_end - pos_az_init +1
        quantEL = pos_el_end - pos_el_init +1
        quantFreq = ((frequencia_end - frequencia_init) / incremento) +1
        tempo_coletas = media_num * 0.2

        tempo_total = (quantAZ * quantEL * quantFreq * tempo_coletas * timer * voltas)/3600
        quantidade_linhas = (quantAZ * quantEL * quantFreq * voltas)
        tempo_por_linhas = (quantAZ * quantEL * quantFreq *
                            tempo_coletas * timer * voltas) / quantidade_linhas
        print(f'\nO tempo estimado do Teste é de {tempo_total} horas.\n')
        print(f'O teste registrará uma linha a cada {tempo_por_linhas} segundos.\n')
        print(f'O arquivo ficará com {quantidade_linhas} linhas.\n')
        
        if input("Digite 'y' para continuar 'n' para alterar os parametros: ") == "y":
            for teste in range(voltas):
                print(f'Teste numero {teste + 1}')
                TesteAda().ada_teste(pos_az_init, pos_az_end, pos_el_init, pos_el_end,
                             media_num, frequencia_init, frequencia_end, timer, NomeArquivo, incremento)
        else:
            self.Inicio()

if __name__ == '__main__':
    
    print("Inicio Teste Lobulo de irradiacao: ")
  
    TesteAda().Inicio()

#    for teste in voltas:
#        print(f'teste {teste}'

#    TesteAda().ada_teste(6.00, 6.00, 0.00, 20, frequencia, 5, -40)

#pos_az_init,pos_az_end,pos_el_init,pos_el_end,media_num,frequencia_init,frequencia_end,timer,TX_power,NomeArquivo
