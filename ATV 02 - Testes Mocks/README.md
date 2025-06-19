# ATV02 - Testes de Integração e Mocks

## Visão Geral

Esta pasta contém a atividade 02 da disciplina de Engenharia de Software 2, dedicada à implementação, padronização e condução de testes de integração, testes utilizando mocks e à aplicação de práticas de TDD (Test Driven Development). O foco é garantir que os diferentes módulos do sistema interajam corretamente entre si, mesmo quando dependências externas são simuladas, e incentivar o desenvolvimento orientado a testes.

## Estrutura da Pasta

- `src/` — Implementação das funcionalidades a serem testadas.
- `tests/` — Testes automatizados, incluindo testes de integração e testes com mocks.
- `requirements.txt` — Dependências necessárias para rodar a atividade e os testes.

## Práticas de TDD (Test Driven Development)

O desenvolvimento orientado a testes (TDD) é incentivado nesta atividade. A abordagem consiste nos seguintes passos:

1. **Escrever o teste antes da implementação:** Antes de criar ou alterar qualquer funcionalidade em `src/`, um teste correspondente deve ser escrito em `tests/`, cobrindo o comportamento esperado.
2. **Executar o teste:** O teste deve falhar, pois a funcionalidade ainda não foi implementada.
3. **Implementar a funcionalidade:** O código em `src/` é desenvolvido ou ajustado para passar no teste.
4. **Executar novamente o teste:** Agora o teste deve passar, comprovando que a funcionalidade atende ao comportamento esperado.
5. **Refatorar:** O código pode ser melhorado, mantendo todos os testes passando.

Esta prática garante que o código seja desenvolvido de maneira incremental, com alta cobertura de testes e menor risco de regressões.

## Tipos de Testes

### Testes de Integração

- Avaliam a interação entre múltiplos módulos ou componentes do sistema.
- Podem envolver a chamada de mais de uma função, classe ou módulo, verificando o funcionamento conjunto.
- São importantes para detectar problemas que não aparecem em testes unitários, como incompatibilidades de interface e integração real dos fluxos de dados.

### Testes com Mocks

- Utilizam a biblioteca `unittest.mock` (ou similar) para simular dependências externas, como APIs, bancos de dados e arquivos.
- Permitem testar fluxos de integração mesmo quando dependências reais não estão disponíveis ou não devem ser acionadas durante o teste.
- Facilitam a criação de cenários controlados, como respostas específicas de serviços externos ou simulação de falhas.

## Padronização e Condução dos Testes

### Organização

- Todos os testes estão no diretório `tests/`, nomeados conforme o módulo ou fluxo testado: `test_<modulo_ou_fluxo>.py`.
- Funções de teste seguem o padrão `test_<cenario>`, explicitando o comportamento esperado.
- Testes com mocks são devidamente identificados por nomes e docstrings descritivos, explicando o motivo da simulação.

### Ferramentas Utilizadas

- **Pytest:** Framework principal para execução dos testes.
- **unittest.mock:** Para criação de mocks, spies e stubs.
- **pytest-cov:** Para análise de cobertura de testes.

### Convenções

- **Isolamento:** Dependências externas são sempre simuladas com mocks nos testes de integração, garantindo que apenas a integração entre os módulos internos seja avaliada.
- **Clareza:** Nomes de testes e docstrings explicam claramente o objetivo e o cenário de cada teste.
- **Reprodutibilidade:** Os testes devem rodar da mesma forma em qualquer ambiente configurado com o `requirements.txt`.

#### Exemplos

**Teste de Integração:**
```python
def test_fluxo_completo_processamento():
    resultado = processar_e_salvar_dados([1, 2, 3])
    assert resultado == "sucesso"
```

**Teste de Integração com Mock:**
```python
from unittest.mock import Mock
from src.meu_modulo import processar_dados_externos

def test_processar_dados_externos_com_api_mockada():
    api_mock = Mock()
    api_mock.obter_dados.return_value = {"status": "ok"}
    resposta = processar_dados_externos(api_mock)
    assert resposta == "ok"
```

**Fluxo TDD:**
```python
# 1. Escreva o teste:
def test_exemplo_comportamento():
    # esperado: funcao retorna valor processado corretamente
    ...

# 2. Execute e veja falhar;
# 3. Implemente em src/;
# 4. Execute e veja passar;
# 5. Refatore mantendo o teste passando.
```

## Execução dos Testes

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute todos os testes:
   ```bash
   pytest
   ```
3. Para gerar um relatório de cobertura (opcional):
   ```bash
   pytest --cov=src
   ```

## Recomendações

- Sempre que um teste de integração envolver dependências externas, utilize mocks para simular o comportamento dessas dependências.
- Cubra cenários de sucesso e falha, incluindo respostas inesperadas ou exceções.
- Mantenha os testes claros, independentes e bem documentados.
- Siga o ciclo do TDD para garantir qualidade e cobertura desde o início do desenvolvimento.

## Boas Práticas

- Uso mocks para simular apenas dependências externas ou complexas.
- Utilização fixtures do pytest para preparar estados de teste, quando necessário.
