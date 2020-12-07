## Python 'Thingiverse Extractor'

Esse é um script para a extração automatica de dados do Thingiverse. O Script coleta informações de projetos de impressão 3d hospedados no Thingiverse e as salva em arquivos no Google Drive.

### Como configurar o Projeto:

Para executar o projeto você precisará do Python versão 3.5 ou mais recente, bem como o gerenciador de pacotes pip. Além disso, os comandos aqui mostrados são executados com o auxílio do [virtualenv](https://virtualenv.pypa.io/en/latest/). Siga então os seguintes passos.

1. Clone este repositório
2. Crie um _virtual env_ do Python com o comando `virtualenv nomeDoViertualenv`, onde `nomeDoVirtualenv` é um nome de sua escolha.
3. Inicie o _virtual env_ com o comando `source nomeDoViertualenv/bin/activate` no Mac/Linux, onde `nomeDoViertualenv` é o nome escolhido no passo anterior.
4. Intstale as dependências do projeto com o comando `pip install -r requirements.txt`
5. Tudo pronto!

### Como executar o script:

Para executar o script basta executar o comando `python . projetoId`, onde `projetoId` é o identificador numérico do projeto no Thingiverse, ou sua URL.

Caso seja a primeira execução do script, uma janela do navegador será mostrada para que se autentique na sua conta do Google e conceda ao script permissão para que acesse seu Drive.
