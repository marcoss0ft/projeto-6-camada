from suaBibSignal import *
import peakutils  # Biblioteca para identificação de picos
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

# Função para converter intensidade em dB, caso seja necessário
def todB(s):
    sdB = 10 * np.log10(s)
    return sdB

# Função principal do receptor
def main():
    #***************************** Instruções ********************************
    
    # Cria um objeto da classe da biblioteca fornecida
    signal = signalMeu()
    
    # Define os parâmetros da gravação de áudio
    fs = 44100  # Taxa de amostragem
    sd.default.samplerate = fs
    sd.default.channels = 1  # Definir 1 canal para mono
    duration = 5  # Duração da gravação em segundos
    numAmostras = int(duration * fs)  # Número de amostras a serem captadas
    
    # Aviso antes de iniciar a gravação
    print(f"Captação do áudio começará em 3 segundos.")
    time.sleep(3)  # Aguarda 3 segundos antes de iniciar a gravação
    
    print("Gravação iniciada...")
    
    # Inicia a gravação de áudio
    audio = sd.rec(numAmostras, samplerate=fs, channels=1)
    sd.wait()  # Aguarda o fim da gravação
    print("Gravação finalizada.")
    
    # Processando o áudio gravado
    dados = audio[:, 0]  # Captura os dados do canal 0, se for estéreo, ficaria apenas um canal
    
    # Cria o vetor de tempo correspondente às amostras
    t = np.linspace(0, duration, numAmostras)
    
    # Plotando o áudio gravado no domínio do tempo
    plt.figure()
    plt.plot(t, dados)
    plt.title("Áudio Gravado - Domínio do Tempo")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()
    
    # Realiza a Transformada de Fourier do sinal de áudio gravado
    print("Calculando a FFT do sinal gravado...")
    xf, yf = signal.calcFFT(dados, fs)
    
    # Plotando o resultado da Transformada de Fourier
    plt.figure()
    plt.plot(xf, np.abs(yf))
    plt.title("FFT do Sinal Gravado - Domínio da Frequência")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()
    
    # Identificação dos picos na FFT
    indices = peakutils.indexes(np.abs(yf), thres=0.2, min_dist=50)
    frequencias_pico = xf[indices]  # Pega as frequências correspondentes aos picos
    print(f"Frequências dos picos detectados: {frequencias_pico}")
    
    # Frequências DTMF (Tabela de frequências)
    frequencias_dtmf = {
        '1': (679, 1209), '2': (679, 1336), '3': (679, 1477),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
        '7': (825, 1209), '8': (825, 1336), '9': (825, 1477),
        '0': (941, 1336)
    }
    
    # Função auxiliar para encontrar a tecla com base nas frequências dos picos
    def encontrar_tecla(frequencias_pico):
        for tecla, (f1, f2) in frequencias_dtmf.items():
            if any(np.isclose(frequencias_pico, f1, atol=10)) and any(np.isclose(frequencias_pico, f2, atol=10)):
                return tecla
        return None

    # Identificando a tecla pressionada com base nos picos
    tecla = encontrar_tecla(frequencias_pico)
    if tecla:
        print(f"Tecla detectada: {tecla}")
    else:
        print("Nenhuma tecla correspondente foi detectada.")
    
    # Exibe todos os gráficos
    plt.show()

if __name__ == "__main__":
    main()
