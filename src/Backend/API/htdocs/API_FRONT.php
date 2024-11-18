<!DOCTYPE html>
<html lang="pt">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preços de Combustíveis</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <h1>API Preços de Combustíveis</h1>
    <div class="grid-container">
        <div class="filter-section">
            <h3>Estado</h3>
            <label for="state">Estado:</label>
            <select id="state" name="state">
                <option value="">Todos</option>
                <option value="SP">SP</option>
                <option value="DF">DF</option>
                <option value="BA">BA</option>
                <option value="RJ">RJ</option>
                <option value="MG">MG</option>
                <option value="RS">RS</option>
                <option value="PR">PR</option>
                <option value="AC">AC</option>
                <option value="AL">AL</option>
                <option value="AM">AM</option>
                <option value="AP">AP</option>
                <option value="CE">CE</option>
                <option value="ES">ES</option>
                <option value="GO">GO</option>
                <option value="TO">TO</option>
                <option value="MA">MA</option>
                <option value="MS">MS</option>
                <option value="MT">MT</option>
                <option value="PA">PA</option>
                <option value="PB">PB</option>
                <option value="PE">PE</option>
                <option value="PI">PI</option>
                <option value="SC">SC</option>
                <option value="RN">RN</option>
                <option value="RO">RO</option>
                <option value="RR">RR</option>
                <option value="SE">SE</option>
            </select>
        </div>
        <div class="filter-section">
            <h3>Tipo de Combustível</h3>
            <label for="fuel_type">Tipo de Combustível:</label>
            <select id="fuel_type" name="fuel_type">
                <option value="">Geral</option>
                <option value="Gasolina">Gasolina</option>
                <option value="Etanol">Etanol</option>
                <option value="Diesel">Diesel</option>
                <option value="GNV">GNV</option>
            </select>
        </div>
        <div class="filter-section">
            <h3>Ano</h3>
            <label for="year">Ano:</label>
            <select id="year" name="year">
                <option value="">Todos</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
                <option value="2021">2021</option>
                <option value="2020">2020</option>
                <option value="2019">2019</option>
                <option value="2018">2018</option>
                <option value="2017">2017</option>
                <option value="2016">2016</option>
                <option value="2015">2015</option>
                <option value="2014">2014</option>
                <option value="2013">2013</option>
                <option value="2012">2012</option>
                <option value="2011">2011</option>
                <option value="2010">2010</option>
                <option value="2009">2009</option>
                <option value="2008">2008</option>
                <option value="2007">2007</option>
                <option value="2006">2006</option>
                <option value="2005">2005</option>
                <option value="2004">2004</option>

            </select>
            <div class="filter-section">
                <h3>Mês</h3>
                <label for="month">Mes</label>
                <select name="month" id="month">
                    <option value="">Todos</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                    <option value="9">9</option>
                    <option value="10">10</option>
                    <option value="11">11</option>
                    <option value="12">12</option>

                </select>
            </div>

        </div>
    </div>
    <div class="button-container">
        <button onclick="consultarAPI()">CONSULTAR API</button>
    </div>

    <div id="chartContainer">
        <h3>Resultados:</h3>
        <div id="resultados"></div>
        <canvas id="chartCanvas" width="400" height="200"></canvas>
    </div>
    <script>
        function consultarAPI() {
            const state = document.getElementById('state').value;
            const fuelType = document.getElementById('fuel_type').value;
            const year = document.getElementById('year').value;
            const month = document.getElementById('month').value;

            const stateParam = (state && state !== "Todos") ? `"${state}"` : "";
            const fuelTypeParam = (fuelType && fuelType !== "GERAL") ? `"${fuelType}"` : "";
            const yearParam = year !== "Todos" ? year : "";
            const monthParam = month !== "Todos" ? month : "";

            const url = `http://127.0.0.1:5000/api/consulta?estado=${stateParam}&produto=${fuelTypeParam}&ano=${yearParam}&mes=${monthParam}`;

            console.log(url);

            fetch(url)
                .then(response => response.json())
                .then(data => {

                    let html = "<table border='1'><tr><th>Estado</th><th>Produto</th><th>Ano</th><th>Mês</th><th>Preço Médio</th></tr>";
                    if (data.length > 0) {
                        data.forEach(row => {
                            html += `<tr>
                            <td>${row.estado_sigla || row['Estado...Sigla']}</td>
                            <td>${row.produto || row['Produto']}</td>
                            <td>${row.ano || row['Ano']}</td>
                            <td>${row.mes || row['Mes']}</td>
                            <td>${row.media_mensal_valor_venda || row['Media_mensal_valor_venda']}</td>
                        </tr>`;

                        });
                    } else {
                        html += "<tr><td colspan='5'>Nenhum dado encontrado.</td></tr>";
                    }
                    html += "</table>";
                    document.getElementById('resultados').innerHTML = html;
                })
                .catch(error => {
                    console.error('Erro ao consultar a API:', error);
                    document.getElementById('resultados').innerHTML = "<p>Erro ao consultar a API.</p>";
                });
        }

        
    </script>

    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        $state = $_GET['state'] ?? '';
        $fuel_type = $_GET['fuel_type'] ?? '';
        $year = $_GET['year'] ?? '';
        $month = $_GET['month'] ?? '';

        $url = "http://127.0.0.1:5000/api/consulta?estado=$state&produto=$fuel_type&ano=$year&mes=$month";

        $response = @file_get_contents($url);

        if ($response === FALSE) {
            echo "<p>Erro ao conectar-se à API.</p>";
        } else {
            $data = json_decode($response, true);

            if (isset($data['error'])) {
                echo "<p>Erro da API: " . htmlspecialchars($data['error']) . "</p>";
            } else {
                echo "<p>DADOS PRONTOS</p>";
            }
        }
    }
    ?>

</body>

</html>