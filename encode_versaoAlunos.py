from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


frequencias_dtmf = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '0': (941, 1336)
}


def todB(s):
    sdB = 10 * np.log10(s)
    return sdB


def gerar_sinal_dtmf(tecla, duration=2, samplerate=44100):
    f1, f2 = frequencias_dtmf[tecla] 
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)  
    senoide1 = np.sin(2 * np.pi * f1 * t) 
    senoide2 = np.sin(2 * np.pi * f2 * t)  
    sinal = senoide1 + senoide2  
    return sinal, t


def main():
    print("Inicializando encoder")
    print("Aguardando usuário")
    

    tecla = input("Digite um número de 0 a 9: ")
    if tecla not in frequencias_dtmf:
        print("Tecla inválida! Digite um número de 0 a 9.")
        return
    
    print("Gerando Tons base")
    

    duration = 2
    fs = 44100  
    tone, t = gerar_sinal_dtmf(tecla, duration, fs)
    
    print(f"Executando as senoides (emitindo o som) para a tecla: {tecla}")
    sd.play(tone, fs) 
    sd.wait()  
    

    print("Gerando gráfico do sinal no domínio do tempo")
    plt.figure()
    plt.plot(t[:1000], tone[:1000]) 
    plt.title(f"Sinal DTMF no tempo - Tecla {tecla}")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()


    signal = signalMeu()  
    print("Gerando FFT e plotando gráfico das frequências emitidas")
    signal.plotFFT(tone, fs)  
    plt.show()

    return  

if __name__ == "__main__":
    main()
