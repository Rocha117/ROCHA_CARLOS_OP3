import investpy
import pandas as pd
import numpy as np
import talib
import mplfinance as mpf


pd.set_option("min_rows", None)
pd.set_option("max_rows", 100)


def extraer(cond, stock_valor, pais, pi="", pf=""):
    """
    Se extraen los datos del precio final diaro del valor 
    """
    if cond == 1:
        # Se extraen los datos del precio final diario del valor en el rango de días dado
        df = investpy.get_stock_historical_data(
            stock_valor, pais, pi, pf)
    else:
        # Se extraen los datos del precio final diario del valor en el último mes del valor
        df = investpy.get_stock_recent_data(
            stock_valor, pais, as_json=False, order='ascending')

    return df


class Indicador_tecnico:
    """
    Permite especificar el indicador tecnico para analizar el activo
    """
    # Aca se usara el paquete talib

    def __init__(self, DataStock, RSI=0, SMA=0):
        self.DataStock = DataStock
        self._RSI = RSI
        self._SMA = SMA

    def RSI(self):
        # Obtener Relative Strength Index (RSI)
        self.DataStock["RSI"] = talib.RSI(
            self.DataStock["Close"], timeperiod=8)
        self._RSI = 1

    def SMA(self):
        # Obtener Simple Moving Average (SMA)
        self.DataStock["SMA"] = talib.SMA(
            self.DataStock["Close"], timeperiod=8)
        self._SMA = 1

    def All(self):
        # Obtener ambos indicadores
        self.DataStock["SMA"] = talib.RSI(
            self.DataStock["Close"], timeperiod=8)
        self.DataStock["RSI"] = talib.SMA(
            self.DataStock["Close"], timeperiod=8)
        self._RSI = 1
        self._SMA = 1


def Grafico(indicadorTec, numSubplots1, numSubplots2, vr=None, pi=None, pf=None):
    """
    Permite hacer la gráfica del activo en un periodo de tiempo
    """

    fig = mpf.figure(figsize=(12, 9))
    s = mpf.make_mpf_style(base_mpf_style='yahoo', y_on_right=False)

    if numSubplots1 == 1 and numSubplots2 == 0:

        ax1 = fig.add_subplot(2, 2, 2, style=s)
        ax11 = ax1.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['RSI'], ax=ax11, ylabel='RSI')
        vol = fig.add_subplot(2, 2, 4, sharex=ax1, style=s)
        mpf.plot(indicadorTec.DataStock,  volume=vol, ax=ax1,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador RSI')

    elif numSubplots1 == 0 and numSubplots2 == 1:

        ax2 = fig.add_subplot(2, 2, 2, style=s)
        ax22 = ax2.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['SMA'], ax=ax22, ylabel='SMA')
        vol = fig.add_subplot(2, 2, 4, sharex=ax2, style=s)
        mpf.plot(indicadorTec.DataStock,  volume=vol, ax=ax2,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador SMA')

    elif numSubplots1 == 1 and numSubplots2 == 1:

        ax1 = fig.add_subplot(2, 2, 2, style=s)
        ax11 = ax1.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['RSI'], ax=ax11, ylabel='RSI')

        mpf.plot(indicadorTec.DataStock,   ax=ax1,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador RSI')

        ax2 = fig.add_subplot(2, 2, 4, style=s)
        ax22 = ax2.twinx()
        ap = mpf.make_addplot(
            indicadorTec.DataStock['SMA'], ax=ax22, ylabel='SMA')

        mpf.plot(indicadorTec.DataStock, ax=ax2,
                 addplot=ap, xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica de valor con indicador SMA')

    if pi == None and pf == None:
        axp = fig.add_subplot(2, 2, 1, style=s)
        volp = fig.add_subplot(2, 2, 3, sharex=axp, style=s)
        mpf.plot(indicadorTec.DataStock, ax=axp, volume=volp,
                 xrotation=10, ylabel='Precio', type='candle', axtitle='Gráfica del valor (últimos 30 días) ')
        mpf.show()

    else:
        axp = fig.add_subplot(2, 2, 1, style=s)
        volp = fig.add_subplot(2, 2, 3, sharex=axp, style=s)
        mpf.plot(indicadorTec.DataStock, ax=axp, volume=volp,
                 xrotation=10, ylabel='Precio', type='candle', axtitle=f'Gráfica del valor (De {pi} a {pf}) ')
        mpf.show()


class Valor:
    """
    Es la base de datos de los valores guardados 
    """
    # Guarda diferentes valores en un diccionario y muestra los diferentes graficos con los diferentes indicadores tecnicos consultados
    valor = {}

    def __init__(self, valor={}):
        self.valor = valor

    def agregar_valor(self, valo, dfIndicador):
        existe = 0
        for key in self.valor.keys():
            if valo == key:
                existe = 1
                break
            else:
                existe = 0

        if existe == 1:
            global num_exis
            num_exis = 1
            return num_exis
        elif existe == 0:
            self.valor.update({valo: dfIndicador})

    def mostrar_valor(self, v1):
        existe = 0

        for key in self.valor.keys():
            if v1 == key:
                existe = 1
                break
            else:
                existe = 0
        if existe == 1:
            print(f"\n{v1}:\n {self.valor[v1].DataStock}\n")
            return self.valor[v1], self.valor[v1]._RSI, self.valor[v1]._SMA
        elif existe == 0:

            print("\nNo está registrado ese valor en el historial de búsquedas\n")


def señal(indicador, nombre, pais):
    rec = ''
    if indicador == 1:
        data = investpy.technical_indicators(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'
        return nombre, data.loc[0, 'value'], rec

    elif indicador == 2:
        data = investpy.moving_averages(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'sma_signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'
        return nombre, data.loc[0, 'sma_value'], rec

    elif indicador == 3:
        data = investpy.technical_indicators(
            name=nombre, country=pais, product_type='stock', interval='daily')
        data2 = investpy.moving_averages(
            name=nombre, country=pais, product_type='stock', interval='daily')
        if data.loc[0, 'signal'] == 'sell':
            rec = 'vender'
        else:
            rec = 'comprar'

        if data2.loc[0, 'sma_signal'] == 'sell':
            rec2 = 'vender'
        else:
            rec2 = 'comprar'

        return nombre, data.loc[0, 'value'], rec, data2.loc[0, 'sma_value'], rec2


def main():
    """
    Despliega un menú de opciones en la consola del terminal
    """
    ot1 = 0
    ValorGrafico = Valor()

    while ot1 == 0:
        # Primer while principal para la identificación del código y el país del valor
        global num_exis
        num_exis = 0
        a = -1

        while a != 1 and a != 2 and a != 3:
            # Bucle que repite la opción de la elección de lista
            print("\n\nEste programa realiza recomendaciones de compra o venta de un valor según un análisis técnico con los datos obtenidos de Investing.com\n")
            print("(1)          Ver lista de países                         ")
            print("(2)          Ver lista de valores de todos los países    ")
            print("(3)          Ver lista de valores según el país          ")
            a = int(input("\n¿Qué desea hacer?\n"))
        if a == 1:
            # Se imprimen todos los países que están registrados en el mercado de valores
            for i in investpy.get_stock_countries():
                print("País {}: {}".format(
                    investpy.get_stock_countries().index(i)+1, i))

        elif a == 2:
            # Se imprime un panda.DataFrame de todos los valores sin importar el país
            print(investpy.get_stocks(country=None))

        elif a == 3:
            # Se imprime un panda.DataFrame de todos los valores según el país indicado
            otra = 1
            while otra != 0:
                try:
                    b = input("Escribe el país de donde quieres buscar:\n")
                    print(investpy.get_stocks(country=b))
                    otra = 0

                except ValueError:
                    # Evita que se ejecute el error ValueError cuando la palabra insertada no se encuentra entre los países de la lista
                    print("Escribe un pais existente\n")

        ott = 1
        while ott != 0:
            # Permite la opción de salida del primer bucle while principal
            ot = str(input("¿Desea ver otra lista? Sí(S) o No (N):\n"))
            if ot == 'S' or ot == 's':
                ot1 = 0
                ott = 0
            elif ot == 'N' or ot == 'n':
                ot1 = 1
                ott = 0
            else:
                ott = 1

    ot2 = 0
    while ot2 == 0:
        # Segundo while principal para ingresar el país y el valor, o salir del programa
        a1 = -1
        while a1 != 1 and a1 != 2:
            # Bucle que repite la opción de la elección de continuar con el análisis o salir del programa
            print(
                "\nElija si desea realizar un análisis técnico de un valor en el mercado de valores\n")
            print("(1)          Analizar un valor                           ")
            print("(2)          Salir                                       ")
            a1 = int(input("\n¿Qué desea hacer?\n"))
        if a1 == 1:
            # Se ingresa el país y el valor para su análisis técnico
            otr = 1
            while otr != 0:
                try:
                    print("¿Qué valor deseas ver?\n")
                    pais = input(
                        "Ingresa el país                 (Segunda columna en la lista de valores)\n")
                    stock_valor = input(
                        "Ingresa el código del valor     (Séptima columna en la lista de valores)\n").upper()
                    p = 0
                    while p == 0:
                        # Permite la opción de especificar un rango de tiempo
                        p1 = str(
                            input("¿Desea establecer un rango de tiempo? Sí(S) o No (N):\n"))
                        if p1 == 'S' or p1 == 's':
                            print(
                                "Escriba el rango de tiempo con el formato (dd/mm/aaaa)")
                            pi = str(input("Escriba el día de inicio :     "))
                            pf = str(input("Escriba el día de término:     "))
                            df = extraer(1, stock_valor, pais, pi, pf)
                            print(df)
                            mpf.plot(df, axtitle=f'Gráfica del valor (De {pi} a {pf})', style='yahoo',
                                     xrotation=15, type='candle')
                            mpf.show()

                            p = 1
                        elif p1 == 'N' or p1 == 'n':
                            df = extraer(2, stock_valor, pais)
                            print(df)
                            mpf.plot(df, axtitle='Gráfica del valor (últimos 30 días)', style='yahoo',
                                     xrotation=15, type='candle')
                            mpf.show()

                            p = 1
                        else:
                            p = 0

                    otr = 0
                except ValueError:
                    print("Escribe un país existente\n")

        elif a1 == 2:
            # Sale del programa
            break

        otq = 0
        while otq == 0:
            z = -1
            while z != 1 and z != 2 and z != 3:
                # Bucle que repite la opción de la elección de indicador
                print("\n¿Cuál indicador deseas ver?\n")
                print(
                    "(1)          RSI (Relative Strength Index)                        ")
                print(
                    "(2)          SMA (Simple Moving Average)                          ")
                print(
                    "(3)          Ambos                                                ")

                z = int(input("\n¿Qué desea hacer?\n"))
            indic1 = Indicador_tecnico(df)
            if z == 1:
                indic1.RSI()
                t = "RSI"

            elif z == 2:
                indic1.SMA()
                t = "SMA"

            elif z == 3:
                indic1.All()

            Grafico(indic1, indic1._RSI, indic1._SMA)
            señ1 = señal(z, stock_valor, pais)
            if z != 3:

                print(
                    f"\n\nEl indicador {t} en el valor búrsatil '{señ1[0]}' es de {señ1[1]}, e indica que se recomienda {señ1[2]}.\n\n")
            else:
                print(
                    f"\n\nCon el valor búrsatil '{señ1[0]}', con el indicador RSI, el cual es de {señ1[1]}, recomienda {señ1[2]}; mientras que el indicador SMA, el cual es de {señ1[3]}, recomienda {señ1[4]}.\n\n")

            ott2 = 1
            while ott2 != 0:
                # Permite la opción de salida del bucle while
                otp = str(
                    input("¿Desea ver otro indicador? Sí(S) o No (N):\n")).upper()
                if otp == 'S':
                    otq = 0
                    ott2 = 0
                elif otp == 'N':
                    otq = 1
                    ott2 = 0
                else:
                    ott2 = 1

        ValorGrafico.agregar_valor(stock_valor, indic1)

        otw = 0
        while otw == 0:
            ddd = 1
            while ddd != 0:
                # Permite la opción de salida del bucle while
                otp5 = str(
                    input("¿Desea ver algún valor registrado? Sí(S) o No (N):\n")).upper()
                if otp5 == 'S':
                    otw = 0
                    ddd = 0
                elif otp5 == 'N':
                    otw = 1
                    ddd = 0
                    break
                else:
                    ddd = 1
            if otp5 == 'S':
                valReg = str(
                    input("Escriba el símbolo del valor registrado que quiere buscar:    ")).upper()
                VR = ValorGrafico.mostrar_valor(valReg)
            elif otp5 == 'N':
                break

            Grafico(VR[0], VR[1], VR[2])

            if VR[1] == 1 and VR[2] == 0:
                t1 = "RSI"
                z1 = 1
            elif VR[1] == 0 and VR[2] == 1:
                t1 = "SMA"
                z1 = 2
            elif VR[1] == 1 and VR[2] == 1:
                z1 = 3
            señ2 = señal(z1, valReg, pais)
            if z1 != 3:

                print(
                    f"\n\nEl indicador {t1} en el valor búrsatil '{señ2[0]}' es de {señ2[1]}, e indica que se recomienda {señ2[2]}.\n\n")
            else:
                print(
                    f"\n\nCon el valor búrsatil '{señ2[0]}', con el indicador RSI, el cual es de {señ2[1]}, recomienda {señ2[2]}; mientras que el indicador SMA, el cual es de {señ2[3]}, recomienda {señ2[4]}.\n\n")
            ott2 = 1
            while ott2 != 0:
                # Permite la opción de salida del bucle while
                otp7 = str(
                    input("¿Desea ver otro valor registrado? Sí(S) o No (N):\n"))
                if otp7 == 'S' or otp7 == 's':
                    otw = 0
                    ott2 = 0
                elif otp7 == 'N' or otp7 == 'n':
                    otw = 1
                    ott2 = 0
                    break
                else:
                    ott2 = 1

                valReg = str(
                    input("Escriba el símbolo del valor registrado que quiere buscar:    ")).upper()
                ValorGrafico.mostrar_valor(valReg)
                VR1 = ValorGrafico.mostrar_valor(valReg)
                Grafico(VR1[0], VR1[1], VR1[2])

                if VR1[1] == 1 and VR1[2] == 0:
                    t2 = "RSI"
                    z2 = 1
                elif VR1[1] == 0 and VR1[2] == 1:
                    t2 = "SMA"
                    z2 = 2
                elif VR1[1] == 1 and VR1[2] == 1:
                    z2 = 3
                    señ3 = señal(z2, valReg, pais)
                if z2 != 3:

                    print(
                        f"\n\nEl indicador {t2} en el valor búrsatil '{señ3[0]}' es de {señ3[1]}, e indica que se recomienda {señ3[2]}.\n\n")
                else:
                    print(
                        f"\n\nCon el valor búrsatil '{señ3[0]}', con el indicador RSI, el cual es de {señ3[1]}, recomienda {señ3[2]}; mientras que el indicador SMA, el cual es de {señ3[3]}, recomienda {señ3[4]}.\n\n")

        ott3 = 1
        while ott3 != 0:
            # Permite la opción de salida del segundo bucle while principal
            otp3 = str(input("¿Desea ver otro valor? Sí(S) o No (N):\n"))
            if otp3 == 'S' or otp3 == 's':
                ot2 = 0
                ott3 = 0
            elif otp3 == 'N' or otp3 == 'n':
                ot2 = 1
                ott3 = 0
            else:
                ott3 = 1


if __name__ == '__main__':
    main()
