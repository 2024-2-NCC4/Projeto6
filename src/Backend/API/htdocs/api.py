import io
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import mysql.connector
import requests

app = Flask(__name__)
#Autorizar requisições de origens diferentes
CORS(app)

# Configuração do banco de dados
db_config = {
    'user': 'root',             
    'password': '',             
    'host': 'localhost',        
    'database': 'pi_fpcp'      
}
# Rota teste
@app.route('/', methods=['GET'])
def api():
    return "API RESPONDENDO"

# Rota para buscar dados com base em filtros
@app.route('/api/consulta', methods=['GET'])
def consulta_dados():
    estado = request.args.get('estado')
    produto = request.args.get('produto')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM tabela_1 WHERE 1=1
        """
        query2 = """
            SELECT * FROM tabela_2 WHERE 1=1
        """
        params = []

        
        if estado:
            query += " AND `estado_sigla` = %s"
            query2 += " AND `estado_sigla` = %s"
            params.append(estado)
        if produto:
            query += " AND `Produto` = %s"
            query2 += " AND `Produto` = %s"
            params.append(produto)
        if ano:
            query += " AND `Ano` = %s"
            query2 += " AND `Ano` = %s"
            params.append(ano)
        if mes:
            query += " AND `Mes` = %s"
            query2 += " AND `Mes` = %s"
            params.append(mes)

        
        full_query = f"({query}) UNION ALL ({query2})"

        cursor.execute(full_query, params * 2)  
        resultados = cursor.fetchall()

        
        for resultado in resultados:
            if "estado_sigla" in resultado:
                resultado["estado_sigla"] = resultado.pop("estado_sigla")
            if "Produto" in resultado:
                resultado["produto"] = resultado.pop("Produto")
            if "Ano" in resultado:
                resultado["ano"] = resultado.pop("Ano")
            if "Mes" in resultado:
                resultado["mes"] = resultado.pop("Mes")
            if "Media_mensal_valor_venda" in resultado:
                resultado["media_mensal_valor_venda"] = resultado.pop("Media_mensal_valor_venda")

        cursor.close()
        conn.close()

        return jsonify(resultados)
    except mysql.connector.Error as err:
        print(f"Erro de conexão ou consulta ao banco de dados: {err}")
        return jsonify({"error": str(err)}), 500






if __name__ == '__main__':
    app.run(debug=True)