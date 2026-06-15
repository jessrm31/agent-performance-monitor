# 🚀 Agent Performance Monitor

Uma ferramenta open source completa para monitorar, analisar e otimizar o desempenho de agentes de IA, com foco especial em **GitHub Copilot Agents** e agentes genéricos.

## ✨ Características Principais

- 📊 **Análise de Desempenho**: Métricas detalhadas de tempo de inferência e consumo de tokens
- 🔍 **Rastreamento por Ferramenta**: Identifique quais ferramentas têm maior desempenho
- 📈 **Dashboard em Tempo Real**: Visualização interativa dos dados de performance
- 💾 **Armazenamento Persistente**: Suporte para múltiplos backends (SQLite, PostgreSQL, MongoDB)
- 📄 **Exportação de Dados**: JSON, CSV, Prometheus, Grafana
- 🔧 **Integração Fácil**: SDKs para Python, JavaScript, REST API
- 📉 **Histórico e Tendências**: Acompanhe a evolução do desempenho ao longo do tempo
- 🤖 **Alertas Inteligentes**: Notificações automáticas de degradação de performance

## 🎯 Casos de Uso

- Monitorar performance do GitHub Copilot em diferentes tipos de tarefas
- Comparar eficiência entre diferentes agentes
- Identificar ferramentas com melhor custo-benefício (tokens consumidos vs qualidade)
- Otimizar pipelines de IA baseado em dados reais
- Detectar anomalias e regressões de performance

## 📦 Arquitetura

```
agent-performance-monitor/
├── backend/                 # Core da aplicação
│   ├── api/                # FastAPI server
│   ├── core/               # Lógica de negócio
│   ├── models/             # Modelos de dados
│   ├── database/           # ORM e migrações
│   └── exporters/          # Exportadores de dados
├── frontend/               # Dashboard web
├── sdk/                    # SDKs de integração
├── cli/                    # Interface de linha de comando
├── docker/                 # Containerização
├── docs/                   # Documentação
└── tests/                  # Testes automatizados
```

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/jessrm31/agent-performance-monitor.git
cd agent-performance-monitor

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações
alembic upgrade head

# Inicie o servidor
python -m backend.api.main
```

### Uso Básico (Python SDK)

```python
from apm_sdk import PerformanceMonitor

monitor = PerformanceMonitor(
    api_url="http://localhost:8000",
    api_key="your-api-key"
)

# Registrar uma execução de agente
monitor.log_execution(
    agent_name="github-copilot-python",
    tool_name="code_generation",
    inference_time_ms=1250,
    tokens_input=450,
    tokens_output=320,
    status="success",
    metadata={"model": "gpt-4", "temperature": 0.7}
)

# Obter métricas
metrics = monitor.get_metrics(
    agent_name="github-copilot-python",
    time_range="24h"
)
print(metrics)
```

### Uso com REST API

```bash
# Registrar execução
curl -X POST http://localhost:8000/api/v1/executions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "agent_name": "github-copilot-python",
    "tool_name": "code_generation",
    "inference_time_ms": 1250,
    "tokens_input": 450,
    "tokens_output": 320,
    "status": "success"
  }'

# Obter métricas agregadas
curl http://localhost:8000/api/v1/metrics/github-copilot-python?time_range=24h \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📊 Métricas Rastreadas

| Métrica | Descrição | Unidade |
|---------|-----------|----------|
| Tempo de Inferência | Tempo total de processamento | ms |
| Tokens Input | Tokens consumidos na entrada | tokens |
| Tokens Output | Tokens gerados na saída | tokens |
| Tokens Totais | Input + Output | tokens |
| Taxa de Sucesso | % de execuções bem-sucedidas | % |
| Latência P50/P95/P99 | Percentis de latência | ms |
| Throughput | Execuções por minuto | req/min |
| Custo Estimado | Custo estimado da execução | USD |

## 🔌 Integrações Suportadas

- ✅ **GitHub Copilot**: Rastreamento nativo de agentes Copilot
- ✅ **Agentes Genéricos**: API agnóstica para qualquer agente
- ✅ **LangChain**: Integração automática com callbacks
- ✅ **LlamaIndex**: Suporte para observabilidade
- ✅ **OpenAI API**: Rastreamento de chamadas diretas
- ✅ **Anthropic API**: Análise de uso Claude
- 🚧 **Azure OpenAI**: Em desenvolvimento
- 🚧 **Hugging Face**: Em desenvolvimento

## 📈 Dashboard

Acesse o dashboard em: `http://localhost:3000`

**Recursos:**
- Gráficos em tempo real de performance
- Comparação entre agentes
- Análise de consumo de tokens
- Heatmaps de utilização de ferramentas
- Exportação de relatórios

## 🛠️ Configuração Avançada

Veja [docs/CONFIGURATION.md](docs/CONFIGURATION.md) para:
- Configurar diferentes backends de banco de dados
- Alertas e notificações
- Autenticação e autorização
- Sampling e agregação de dados
- Retenção de dados

## 📚 Documentação

- [Guia de Instalação](docs/INSTALLATION.md)
- [Integração com GitHub Copilot](docs/COPILOT_INTEGRATION.md)
- [API Reference](docs/API.md)
- [SDK Documentation](docs/SDK.md)
- [CLI Guide](docs/CLI.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🐳 Docker

```bash
# Build da imagem
docker build -t agent-performance-monitor .

# Executar container
docker run -p 8000:8000 -p 3000:3000 agent-performance-monitor
```

Ver [docker/README.md](docker/README.md) para mais detalhes.

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=backend --cov-report=html

# Testes de integração
pytest -m integration
```

## 📝 Exemplos

Veja a pasta [examples/](examples/) para:
- Integração com GitHub Copilot
- Monitoramento de agentes LangChain
- Dashboards personalizados
- Análises avançadas

## 🤝 Contribuindo

Acreditamos no poder da comunidade! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para:
- Como reportar bugs
- Como submeter features
- Processo de Pull Request
- Guia de estilo de código

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade open source
- Contribuidores do projeto
- GitHub por Copilot

## 📞 Suporte

- 📧 Email: support@apm.dev
- 💬 Discussões: [GitHub Discussions](https://github.com/jessrm31/agent-performance-monitor/discussions)
- 🐛 Bugs: [GitHub Issues](https://github.com/jessrm31/agent-performance-monitor/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/jessrm31/agent-performance-monitor/wiki)

## 🌟 Roadmap

- [x] Core de API
- [x] SDK Python
- [x] Dashboard básico
- [ ] SDK JavaScript/TypeScript
- [ ] Integração com Grafana
- [ ] Machine Learning para previsão de performance
- [ ] Otimizações automáticas baseadas em IA
- [ ] Marketplace de plugins

---

**Feito com ❤️ para a comunidade de IA**