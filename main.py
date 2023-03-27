import pandas as pd


def read_excel():
    global vendas_dez_df, vendas_df, gerentes_df
    vendas_df = pd.read_excel('Vendas.xlsx')
    gerentes_df = pd.read_excel('Gerentes.xlsx')
    vendas_dez_df = pd.read_excel('Vendas - Dez.xlsx')


def concat_merge_df():
    global faturamento_total
    pd.set_option('display.max_columns', None)
    vendas_total = pd.concat([vendas_df, vendas_dez_df])

    vendas_gerentes = pd.merge(
        vendas_total, gerentes_df[['ID Loja', 'Gerente']], on='ID Loja')

    faturamento_total = vendas_gerentes.groupby('ID Loja').agg({
        'Gerente': 'first',
        'Valor Final': 'sum',
        'Quantidade': 'sum',
    })
    qtde_venda_loja = vendas_total['ID Loja'].value_counts()
    faturamento_total['N. Vendas'] = faturamento_total.index.map(
        qtde_venda_loja)
    ticket_medio = (faturamento_total['Valor Final'] /
                    faturamento_total['Quantidade'])
    faturamento_total['Ticket Medio'] = faturamento_total.index.map(
        ticket_medio)

    faturamento_total = faturamento_total.reindex(
        columns=['Gerente', 'N. Vendas', 'Valor Final', 'Ticket Medio', 'Quantidade'])


def formatar_df():
    faturamento_total['Valor Final'] = faturamento_total['Valor Final'].map(
        'R${:,.2f}'.format)
    faturamento_total['Ticket Medio'] = faturamento_total['Ticket Medio'].map(
        'R${:,.2f}'.format)


def executar():
    read_excel()
    concat_merge_df()
    formatar_df()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(faturamento_total)


executar()
