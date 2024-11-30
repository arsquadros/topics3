Instruções de uso:

Crie um ambiente virtual Python usando seu método favorito. Eu recomendo o venv ou anaconda.

Dentro do ambiente virtual, instale as dependências necessárias (disponíveis no arquivo requirements.txt). Por exemplo, com o venv: ````pip install -r requirements.txt```

add environment variable to the system as GROK_API_KEY in windows:
```setx GROK_API_KEY "your_api_key_here"``` (necessário reiniciar o terminal)
add environment variable to the system as GROK_API_KEY in linux
```export GROK_API_KEY="your_api_key_here"```

Caso não possua uma chave Grok, é possível criar uma [AQUI](https://console.groq.com/keys) de modo gratuito, só é necessário fazer login.

É possível executar a aplicação em funcionamento no seguinte link: https://assistente-conversacional-as05.streamlit.app/
