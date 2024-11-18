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


@app.route('/api/grafico', methods=['GET'])
def grafico():
    # Construir a URL para a rota /api/consulta com os mesmos parâmetros
    estado = request.args.get('estado')
    produto = request.args.get('produto')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    # Construir a URL da consulta com aspas ao redor dos valores
    consulta_url = f"http://127.0.0.1:5000/api/consulta?estado={estado}&produto={produto}&ano={ano}&mes={mes}"
    
    # Fazer a requisição para a rota /api/consulta usando requests
    response = requests.get(consulta_url)
    if response.status_code != 200:
        return "Erro ao consultar dados", 500

    # Extrair os dados da resposta JSON
    dados = response.json()

    # Verificar se há dados
    if not dados:
        return "Nenhum dado encontrado para os filtros aplicados", 404

    # Preparar os dados para o gráfico
    estados = [item['estado_sigla'] for item in dados]
    precos = [float(item['Media_mensal_valor_venda']) for item in dados]

    # Gerar o gráfico usando Matplotlib
    plt.figure(figsize=(10, 5))
    plt.bar(estados, precos, color='skyblue')
    plt.xlabel('Estado')
    plt.ylabel('Preço Médio de Combustível')
    plt.title('Preço Médio de Combustível por Estado')

    # Salvar o gráfico em um objeto BytesIO em vez de um arquivo
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Voltar ao início do arquivo para leitura

    # Retornar a imagem como uma resposta HTTP
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)




if __name__ == '__main__':
    app.run(debug=True)