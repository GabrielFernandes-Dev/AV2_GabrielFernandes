import mysql.connector

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NBHL84ownD6ihT",
    database="ProcessoPagamento"
)

cursor = mydb.cursor()
# Criando banco de dados para processamento de pagamento, caso não exista
createdb = lambda cursor : cursor.execute("CREATE DATABASE IF NOT EXISTS ProcessoPagamento")
# Criando tabela de conta bancaria com saldo
create_bankaccount_table = lambda cursor : cursor.execute("CREATE TABLE IF NOT EXISTS ContaBanco (id INT AUTO_INCREMENT PRIMARY KEY, saldo DECIMAL(10,2), credito DECIMAL(10,2))")
# Criando tabela de usuario com login e senha para fazer authenticação
create_user_table = lambda cursor : cursor.execute("CREATE TABLE IF NOT EXISTS Usuario (id INT AUTO_INCREMENT PRIMARY KEY, id_conta_banco INT, nome VARCHAR(255), email VARCHAR(255), senha VARCHAR(255), FOREIGN KEY (id_conta_banco) REFERENCES ContaBanco(id))")
# Criando tabela de forma de pagamento
crate_paymentmethod_table = lambda cursor : cursor.execute("CREATE TABLE IF NOT EXISTS FormaPagamento (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255))")
# Criando tabela de pagamento com id do usuario, valor, forma de pagamento e data. O id do usuario é chave estrangeira
create_payment_table = lambda cursor : cursor.execute("CREATE TABLE IF NOT EXISTS Pagamento (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, valor DECIMAL(10,2), id_forma_pagamento INT, data DATE, FOREIGN KEY (id_usuario) REFERENCES Usuario(id), FOREIGN KEY (id_forma_pagamento) REFERENCES FormaPagamento(id))")

create_tables = lambda cursor: [
    func(cursor)
    for func in (createdb, create_bankaccount_table, create_user_table, crate_paymentmethod_table, create_payment_table)
]
create_tables(cursor)

# Processamento de pagamento
# Inicializando a transação
create_transaction = lambda :  "Inicializando a transação"

# Pagamento com dinheiro
recive_cash = lambda valor : f"Pagamento de R${valor} recebido"
print_payment_receipt = lambda id_transacao : f"Recibo do pagamento foi impresso para a transação de id: {id_transacao}"
return_payment_receipt = lambda : "Recibo do pagamento foi entregue ao cliente"

# Pagamento com transferência bancária
provide_bank_deposit_details = lambda id_cliente, valor, cursor : confirm_payment_approval() if verify_bank_account(id_cliente, cursor) >= valor else cancel_transaction()
verify_bank_account = lambda id_cliente, cursor: (
    cursor.execute("SELECT cb.saldo FROM Usuario u INNER JOIN ContaBanco cb ON u.id_conta_banco = cb.id WHERE u.id = %s", (id_cliente,)),
    cursor.fetchone()
)

# Pagamento com cartão de crédito
request_payment_authorization = lambda id_cliente, valor, cursor : True if request_credit_account_datails(id_cliente, cursor) >= valor else False
request_credit_account_datails = lambda id_cliente, cursor : next(iter(cursor.execute("SELECT cb.credito FROM Usuario u INNER JOIN ContaBanco cb ON u.id_conta_banco = cb.id WHERE u.id = %s", (id_cliente,)).fetchone()), None)

# Finalizando a transação
confirm_payment_approval = lambda id_cliente, valor, cursor : complete_transaction() if cursor.execute("UPDATE ContaBanco cb INNER JOIN Usuario u ON cb.id = u.id_conta_banco SET cb.saldo = saldo - %s WHERE u.id = %s", (valor, id_cliente)) else cancel_transaction()
cancel_transaction = lambda : "Transação cancelada"
complete_transaction = lambda : "Transação completada com sucesso"

def main(method, data):
    payment_methods = {
        'cash': lambda : recive_cash(data),
        'transfer': lambda : provide_bank_deposit_details(data[1], data[0], cursor),
        'credit': lambda : request_payment_authorization(data[1], data[0], cursor)
    }
    
    return payment_methods[method]() if method in payment_methods else "Método de pagamento não encontrado"


main('transfer', [150.50, 1])
main('credit', [200.00, 2])

bp = 1
