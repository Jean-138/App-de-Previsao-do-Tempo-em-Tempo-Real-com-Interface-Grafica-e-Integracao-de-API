
Um aplicativo desktop moderno desenvolvido em Python que fornece informações meteorológicas precisas de qualquer cidade do mundo. Integrado com a API OpenWeatherMap, exibe dados em tempo real com interface gráfica atraente.

## Funcionalidades

- Busca de clima por nome de cidade (suporta cidades em português)
- Exibição de temperatura atual, sensação térmica e umidade
- Informações de velocidade do vento e pressão atmosférica
- Previsão estendida para os próximos 5 dias
- Exibição da hora local da cidade selecionada
- Coordenadas geográficas (latitude/longitude)
- Interface gráfica moderna e intuitiva com Tkinter
- Proteção de API key com arquivo .env

## Tecnologias Utilizadas

| Ferramenta | Função |
|-----------|--------|
| Python 3.x | Linguagem principal |
| Tkinter | Interface gráfica desktop |
| OpenWeatherMap API | Dados meteorológicos em tempo real |
| geopy | Conversão de localidades em coordenadas |
| pytz + TimezoneFinder | Gestão de fusos horários |
| Pillow (PIL) | Manipulação e exibição de imagens |
| requests | Requisições HTTP para APIs |
| python-dotenv | Gerenciamento seguro de credenciais |

## Requisitos

- Python 3.7+
- Bibliotecas listadas em requirements.txt
- Chave de API gratuita do OpenWeatherMap (registre-se em https://openweathermap.org/api)

## Como Instalar e Usar

### 1. Clone o repositório
git clone [seu-link-github]
cd Weather-App

### 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Configure a API key
Crie um arquivo .env na raiz do projeto:
WEATHER_API_KEY=sua_chave_aqui

### 5. Execute o aplicativo
python main.py

## Como Usar

1. Inicie o app executando python main.py
2. Digite o nome da cidade no campo de busca (ex: "São Paulo", "Rio de Janeiro")
3. Clique no botão de busca para obter os dados
4. Visualize os dados atualizados com temperatura, umidade, vento e mais
5. Confira a previsão para os próximos 5 dias com ícones visuais

## Estrutura do Projeto

Weather-App/
├── main.py                 # Arquivo principal com lógica do app
├── requirements.txt        # Dependências do projeto
├── .env                    # Arquivo de configuração (não versionado)
├── .gitignore             # Arquivos ignorados pelo Git
├── Images/                # Pasta com ícones de clima
│   ├── logo.png
│   ├── search.png
│   └── ...
└── README.md              # Este arquivo

## Conceitos Técnicos Aplicados

- API REST: Integração com serviço externo para dados em tempo real
- Geolocalização: Conversão de nomes de cidades em coordenadas geográficas
- Fuso Horário Dinâmico: Ajuste automático da hora local de cada cidade
- GUI Responsiva: Interface desktop com Tkinter
- Segurança: Proteção de credenciais com variáveis de ambiente

## Melhorias Futuras

- Tratamento robusto de erros com try/except
- Validação de entrada do usuário
- Suporte a tema claro/escuro
- Histórico de buscas
- Notificações de alertas meteorológicos
- Integração com localização automática do usuário
- Possibilidade de salvar cidades favoritas
- Tradução completa para português

## Licença

Este projeto é de código aberto e disponível sob a licença MIT.


## Contribuições

Sugestões e melhorias são bem-vindas! Abra uma issue ou faça um pull request.
