## 🛠 Estrutura de pastas

-Raiz<br>
|<br>
|-->htdocs<br>
  &emsp;|-->api.py<br>
  &emsp;|-->API_FRONT.php<br>
  &emsp;|-->requirements.txt<br>
  &emsp;|-->style.css<br>
  |-->executáveis<br>
  &emsp;|-->api.py<br>
  


## 🛠 Instalação

<b>Xampp:</b>

Faça o Download do aplicativo <a href="https://godotengine.org/download](https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe">XAMPP</a> no seu computador.

1 - Acesse a pasta C:\xampp, abra a pasta htdocs, copie os arquivos da pasta do projeto para dentro do Xampp.<br><br>
2 - Acesse a pasta C:\xampp\mysql\data, copie a pasta inteira pi_fpcp, e cole dentro.

Dentro do aplicativo, inicie o modulo Apache, MySQL

Abra a pasta htdocs dentro do Xampp, inicie um terminal CMD dentro da pasta, e coloque esse código

```sh
pip install -r requirements.txt
```
<br> E logo depois<br>

```sh
python api.py
```

Após a API estar rodadando, acesse <a href="http://localhost/API_FRONT.php">localhost/API_FRONT.php</a>





