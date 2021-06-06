import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
global x
global max_y

def retorna_valores_de_colunas(todas_colunas, data_frame, ano):
    array_final = []
    for coluna in todas_colunas:
        if coluna == "ANO":
            array_final.insert(0, ano)
        elif data_frame.loc[(ano_agrupado['sgpartido'] == coluna)].empty:
            array_final.insert(0, 0)
        else:
            array_final.insert(0, ano_agrupado.loc[(ano_agrupado['sgpartido'] == coluna)]['vlrliquido'].values[0])
    return list(array_final[::-1])


if __name__ == '__main__':
    pd.set_option('display.max_columns', 29)
    cota_parlamentar = pd.read_csv('cota-parlamentar\\cota-parlamentar.csv')

    valores = {}
    colunas = sorted(cota_parlamentar['sgpartido'].unique())
    colunas.insert(0, "ANO")
    dfObj = pd.DataFrame(columns=colunas)
    min_ano = 2007
    max_ano = 2022

    for i in range(min_ano, max_ano):
        ano = cota_parlamentar.loc[(cota_parlamentar['datemissao'] >= f"{i}-01-01 00:00:00") & (
                cota_parlamentar['datemissao'] <= f"{i}-12-31 99:99:99")]
        ano_agrupado = ano.groupby(['sgpartido'])['vlrliquido'].sum().reset_index(name='vlrliquido').sort_values(
            by='sgpartido', ascending=True)
        valores = retorna_valores_de_colunas(colunas, ano_agrupado, i)
        data_frame_ano = pd.DataFrame([valores], columns=colunas)
        dfObj = dfObj.append(data_frame_ano)
    novas_colunas = ["ANO", "PT", "PSDB", "PMDB", "DEM", "PR", "PSD", "PP", "MDB", "PSB", "PDT", "PTB", "PRB",
                     "PCdoB", "PROS", "PSC",
                     "PODE", "PPS", "SD", "PSL", "PV"]
    max_y = 0
    for coluna in novas_colunas:
        if coluna == "ANO":
            x = dfObj[coluna]
        else:
            y = dfObj[coluna]
            maior_valor_y = max(int(number) for number in y.to_list())
            if maior_valor_y > max_y:
                max_y = maior_valor_y
            plt.plot(x, y, label=coluna)
    plt.xlabel("Ano")
    plt.ylabel("Valores Gastos(x10^7)")
    plt.title("Cotas dos Parlamentares")
    plt.legend(loc=2)
    plt.yticks(np.arange(0, max_y + 1, 10000000))
    plt.xticks(np.arange(min_ano, max_ano, 1))
    plt.show()
