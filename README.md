<img src="https://raw.githubusercontent.com/VictorBrasileiroo/Projeto_Observatorio_de_Permanencia/main/banner.png" alt="Banner" style="width: 100%; max-width: 800px; height: auto;"></img>
# 📊 Observatório de Permanência

## 🌟 Introdução

O **Observatório de Permanência** é uma plataforma completa que combina **Django REST Framework**, **Machine Learning** e um **Dashboard Interativo** para identificar e monitorar o risco de evasão de alunos em instituições de ensino.

A solução foi projetada para **instituições de ensino, universidades e escolas técnicas**, permitindo **analisar dados acadêmicos históricos** e **prever a probabilidade de evasão** para cada estudante, de forma **automatizada e visual**.

***

## 📌 Funcionalidades

- **Cadastro e gestão de estudantes** com dados pessoais e acadêmicos
- **Predição automatizada** de risco de evasão usando modelo de Machine Learning
- **Classificação de risco** em **Baixo**, **Médio** e **Alto**
- **Relatórios gerenciais** com métricas:
    - Cobertura de análises
    - Distribuição de risco
    - Taxa de evasão prevista
    - Probabilidade média de evasão
- **Dashboard responsivo** com gráficos dinâmicos
- **API documentada** via [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- **Deploy simplificado** com Docker e PostgreSQL

***

## 🏗 Arquitetura

```plaintext
┌────────────────────────────────────────────────────┐
│                    Frontend (Web)                  │
│  HTML + CSS + JavaScript (Chart.js)                │
│  - Dashboard interativo                            │
│  - Consome API REST via fetch                      │
└────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│                    Backend (API)                   │
│  Django + Django REST Framework                    │
│  - App "estudantes": CRUD de Estudante             │
│  - App "analises": Predições, relatórios, limpeza  │
│  - Serviço ML: ModeloPredicaoService               │
│  - Autodoc: drf-spectacular                        │
└────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│                 Modelo de Machine Learning         │
│  - Arquivo .pkl treinado (Gradient Boosting)       │
│  - Metadados JSON (features, thresholds, métricas) │
│  - Executa predict_proba() e retorna probabilidade │
└────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│                   Banco de Dados                   │
│  PostgreSQL                                        │
│  - Dados de estudantes                             │
│  - Predições armazenadas                           │
└────────────────────────────────────────────────────┘
```


***

## 🧠 Modelo de Machine Learning

### Algoritmo e Performance

- **Algoritmo**: Gradient Boosting Classifier otimizado
- **Features**: 13 variáveis acadêmicas
- **Validação**: Cross-validation com 5-fold

### Métricas de Desempenho

- **AUC-ROC**: 0.9615
- **PR-AUC**: 0.9583
- **Accuracy**: 90.08%
- **Precision**: 88.40%
- **Recall**: 85.91%
- **F1-Score**: 87.14%
- **Threshold Otimizado**: 0.6102

### Bandas de Risco

- **Baixo Risco**: < 0.3 (Probabilidade < 30%)
- **Médio Risco**: 0.3 - 0.7 (Probabilidade 30-70%)
- **Alto Risco**: > 0.7 (Probabilidade > 70%)

***

## ⚡ Backend

### 🔧 Tecnologias e Padrões

- **Framework**: Django 4.2 + Django REST Framework 3.14
- **ORM**: Django Models com migrations automáticas
- **Serialização**: Django REST Serializers
- **Validação**: Validators customizados + Django Forms
- **Documentação**: drf-spectacular (OpenAPI 3.0)
- **Docker**
- **PostgreSQL**

***

## 🔄 Fluxo de Funcionamento

### 1. Cadastro de Estudantes

- Inserção via API (`/api/estudantes/`) ou painel administrativo
- Validação automática de dados (matrícula)

### 2. Execução das Análises

- `POST /api/analises/analisar_todos_estudantes/` processa lote completo
- Pipeline de ML: preparação → predição → classificação de risco

### 3. Armazenamento Inteligente

- Predições gravadas com timestamp e versionamento
- Histórico mantido para análise temporal
- Campos: `probabilidade`, `previsao`, `nivel_risco`, `confianca`
- Auditoria completa de alterações

### 4. Relatórios Avançados

- Relatórios em tempo real via `GET /api/analises/gerar_relatorio_analises/`
- Métricas de performance do modelo

### 5. Visualização Interativa

- Dashboard atualizado em tempo real
- Gráficos dinâmicos: pizza, barras

***

## 🧠 Deploy

### Subindo o ambiente com Docker 🐳

```bash
docker-compose up --build
```

- **API**: http://localhost:8000/api/
- **Dashboard**: abrir `Dashboar_Evasao/index.html` no navegador

***

## 🗄️ API Endpoints Completa

### Estudantes

| Método | Endpoint | Função |
| :-- | :-- | :-- |
| GET | `/estudantes/` | Lista estudantes |
| POST | `/estudantes/` | Cria estudante |
| GET | `/estudantes/{id}/` | Detalha estudante |
| PUT | `/estudantes/{id}/` | Atualiza estudante |
| DELETE | `/estudantes/{id}/` | Remove estudante |

### Análises

| Método | Endpoint | Função |
| :-- | :-- | :-- |
| POST | `/analises/analisar_todos_estudantes/` | Executa predição |
| GET | `/analises/listar_todas_analises/` | Lista predições |
| DELETE | `/analises/remover_todas_analises/` | Apaga predições |
| GET | `/analises/gerar_relatorio_analises/` | Relatório estatístico |

***

## 💻 Frontend 
### 🎨 Tecnologias e Features

- **Base**: HTML5, CSS3 (Grid/Flexbox), JavaScript ES6+
- **Visualização**: Chart.js 4.x com plugins avançados
- **UI/UX**: Design responsivo
- **Performance**: Lazy loading

*** 

## 🎯 Aplicabilidade Detalhada

### 🏫 Universidades e Faculdades

- **Objetivo**: Reduzir evasão e aumentar taxa de conclusão
- **Implementação**: Integração com sistemas acadêmicos (SigAA, Moodle)
- **Benefícios**:
    - Identificação precoce de estudantes em risco
    - Otimização de programas de apoio estudantil
    - Melhoria dos indicadores institucionais (ENADE, avaliação MEC)
    - ROI: Redução de 15-25% na evasão documentada

### 🔧 Escolas Técnicas e Profissionalizantes

- **Foco**: Cursos técnicos de 2-3 anos com alta taxa de abandono
- **Diferencial**: Análise de adequação vocacional e empregabilidade
- **Métricas específicas**:
    - Correlação entre área técnica e perfil do aluno
    - Impacto de estágios na permanência
    - Inserção no mercado de trabalho

### 💻 Educação a Distância (EAD)

- **Desafio**: Alta taxa de evasão (60-80% em alguns cursos)
- **Solução personalizada**:
    - Análise de engajamento digital (logs, tempo online)
    - Predição baseada em padrões de acesso
    - Triggers automáticos para intervenção

### 🏛️ Órgãos Públicos e Secretarias de Educação

- **Escala**: Análise municipal, estadual ou federal
- **Integração**: Censo Escolar, SISTEC, sistemas estaduais
- **Relatórios macro**:
    - Evasão por região geográfica
    - Impacto de políticas públicas
    - Alocação eficiente de recursos

### 🎓 Programas Sociais e Bolsas

- **Aplicação**: PROUNI, FIES, bolsas institucionais
- **Monitoramento**: Eficácia de programas de apoio
- **Otimização**: Direcionamento inteligente de recursos
- **Compliance**: Prestação de contas automatizada

### 🌐 Redes de Ensino Privadas

- **Multi-unidades**: Dashboard centralizado para dezenas de campi
- **Benchmarking**: Comparação de performance entre unidades
- **Expansão**: Análise de viabilidade de novos cursos/campi
- **Exemplo de implementação**:

***

## 🚀 Melhorias Futuras

### 📈 Versão 2.0 (Próximos 6 meses)

- **IA Generativa**: Relatórios automatizados com insights textuais
- **Mobile App**: Aplicativo nativo para coordenadores

### 🤖 Versão 3.0 (Médio prazo)

- **AutoML**: Retreinamento automático do modelo
- **Predição Temporal**: Quando o aluno pode evadir
- **Recomendações Personalizadas**: IA para sugerir intervenções

***

## 📋 Instalação e Configuração

### Pré-requisitos

- Python 3.9+
- Docker \& Docker Compose
- PostgreSQL 12+

### Configuração Rápida

```bash
# Clone o repositório
git clone https://github.com/VictorBrasileiroo/Projeto_Observatorio_de_Permanencia.git
cd observatorio_de_permanencia

# Suba o ambiente completo
docker-compose up -d --build

```


### Acessos

- **API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **Documentação**: http://localhost:8000/api/docs/
- **Dashboard**: http://127.0.0.1:3000/Dashboard_Evasao/index.html

***

## 🤝 Contribuição

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Desenvolvimento

- Seguir PEP 8 para Python
- Documentar funções com docstrings

***

## 📄 Licença

Este projeto licenciado por MPL-2.0 license.

***

## 📞 Suporte e Contato
- Victor André Lopes Brasileiro - valb1@ic.ufal.br
  
***

**Desenvolvido para combater a evasão estudantil e promover a permanência na educação.**

