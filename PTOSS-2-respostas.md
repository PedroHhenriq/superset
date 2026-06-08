<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# PTOSS-2: Artefatos do Repositório

Este documento registra os artefatos usados na entrega da atividade PTOSS-2,
com foco nas branches preparadas para Pull Requests no Apache Superset.

## Pull Requests Principais

| PR | Branch | Objetivo | Status |
| --- | --- | --- | --- |
| `fix(urls): preserve repeated query parameters` | `fix/modify-url-query-repeated-params` | Corrigir `modify_url_query` para preservar parâmetros repetidos e listas em query strings | Branch preparada para PR oficial |
| `test(version): cover development environment label` | `test/get-dev-env-label` | Adicionar teste unitário para `get_dev_env_label` | Branch preparada para PR oficial |

Os links dos PRs devem ser preenchidos após a abertura no repositório oficial:

| PR | Link |
| --- | --- |
| `fix(urls): preserve repeated query parameters` | A preencher |
| `test(version): cover development environment label` | A preencher |

## Código-Fonte Utilizado

| Branch | Arquivo | Função | Uso na atividade |
| --- | --- | --- | --- |
| `fix/modify-url-query-repeated-params` | `superset/utils/urls.py` | `modify_url_query` | Funcionalidade corrigida por TDD |
| `fix/modify-url-query-repeated-params` | `tests/unit_tests/utils/urls_tests.py` | testes de `modify_url_query` | Testes do ciclo Red/Green/Refactor |
| `test/get-dev-env-label` | `superset/utils/version.py` | `get_dev_env_label` | Código existente exercitado por teste unitário novo |
| `test/get-dev-env-label` | `tests/unit_tests/utils/version_tests.py` | testes de `get_dev_env_label` | Teste unitário compatível com PR upstream |
| `ptoss-2-tdd-cycles` | `.github/workflows/ptoss-backend-tests.yml` | workflow de CI | Execução dos testes e geração de cobertura no fork da equipe |

## Testes Implementados

### PR `fix(urls): preserve repeated query parameters`

Arquivo: `tests/unit_tests/utils/urls_tests.py`.

| Teste | Objetivo |
| --- | --- |
| `test_modify_url_query_preserves_repeated_existing_parameters` | Verifica que parâmetros repetidos existentes, como `filter=a&filter=b`, não são perdidos |
| `test_modify_url_query_adds_list_values_as_repeated_parameters` | Verifica que valores recebidos como lista são serializados como parâmetros repetidos |

### PR `test(version): cover development environment label`

Arquivo: `tests/unit_tests/utils/version_tests.py`.

| Teste | Objetivo |
| --- | --- |
| `test_get_dev_env_label_formats_branch_and_sha` | Cobre combinações de branch/SHA presentes e ausentes |
| `test_get_dev_env_label_prefers_github_environment` | Verifica precedência das variáveis de ambiente do GitHub sobre valores locais |

## Instruções de Execução

### Execução local dos testes dos PRs

Com o ambiente de desenvolvimento do Superset configurado:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/urls_tests.py \
  tests/unit_tests/utils/version_tests.py \
  -q
```

Para executar apenas os testes do PR de URLs:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/urls_tests.py \
  -q
```

Para executar apenas os testes do PR de versionamento:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/version_tests.py \
  -q
```

Antes de enviar branches para o fork de entrega ou abrir PR no Superset:

```bash
pre-commit run --all-files
```

### Execução no GitHub Actions

No fork da equipe, a branch `ptoss-2-tdd-cycles` contém o workflow:

```text
.github/workflows/ptoss-backend-tests.yml
```

Ele pode ser usado para executar os testes e gerar os relatórios de cobertura.
O workflow gera o artefato:

```text
ptoss-coverage-reports
```

Esse artefato contém:

```text
coverage.xml
htmlcov/index.html
```

## Relatórios de Cobertura

A cobertura é gerada pelo workflow `PTOSS Backend Tests` usando `pytest-cov`.
Os relatórios ficam disponíveis como artefato da execução do GitHub Actions.

Resultado registrado em execução anterior do workflow:

| Arquivo | Stmts | Miss | Branch | BrPart | Cobertura |
| --- | ---: | ---: | ---: | ---: | ---: |
| `superset/tasks/utils.py` | 123 | 92 | 70 | 0 | 17% |
| `superset/utils/core.py` | 929 | 587 | 324 | 1 | 29% |
| `superset/utils/oauth2.py` | 113 | 59 | 20 | 0 | 42% |
| `superset/utils/screenshots.py` | 201 | 118 | 24 | 0 | 37% |
| `superset/utils/urls.py` | 32 | 15 | 10 | 0 | 50% |
| `superset/utils/version.py` | 39 | 21 | 14 | 1 | 47% |
| Total dos módulos instrumentados | 1437 | 892 | 462 | 2 | 30% |

Como consultar o relatório:

1. Acessar o fork da equipe no GitHub.
2. Abrir a aba `Actions`.
3. Selecionar a execução do workflow `PTOSS Backend Tests`.
4. Baixar o artefato `ptoss-coverage-reports`.
5. Abrir `htmlcov/index.html` ou consultar `coverage.xml`.

## Histórico de Commits

### Branch `fix/modify-url-query-repeated-params`

| Commit | Papel no processo |
| --- | --- |
| `f148b2f7af test: add failing tests for repeated URL query params` | Red: testes falhando para parâmetros repetidos |
| `4132e0bff6 fix: preserve repeated query params in modify_url_query` | Green: implementação mínima da correção |
| `dac2465266 refactor: use urlencode doseq for query serialization` | Refactor: troca de montagem manual por `urlencode(..., doseq=True)` |
| `d94d0f3a3e style: format URL tests` | Ajuste de formatação exigido pelo pre-commit |

### Branch `test/get-dev-env-label`

| Commit | Papel no processo |
| --- | --- |
| `27842d3f9c test: cover development environment label` | Teste unitário para `get_dev_env_label` |

### Branch `ptoss-2-tdd-cycles`

| Commit | Papel no processo |
| --- | --- |
| `632fea21ec test: add failing tests for repeated URL query params` | Início do TDD para `modify_url_query` |
| `4209369c15 fix: preserve repeated query params in modify_url_query` | Implementação da correção |
| `6969bdf43d refactor: use urlencode doseq for query serialization` | Refatoração mantendo testes aprovados |
| `fe0f9cb453 test: add PTOSS MC/DC unit tests` | Testes unitários adicionais da atividade |
| `c5343d098e ci: add PTOSS backend coverage workflow` | Workflow de execução e cobertura |
| `f74ec5d6d8 test: cover development environment label` | Teste de versionamento incluído na branch da atividade |
| `4bc2e14cc3 ci: include version tests in PTOSS workflow` | Inclusão dos testes de versionamento no workflow |
| `5e04b76bce docs: detail TDD cycles` | Registro intermediário dos ciclos de TDD |
| `docs: simplify PTOSS repository artifacts` | Documentação final dos artefatos da entrega |

## Branches a Enviar ao Fork de Entrega

```bash
git push -u entrega ptoss-2-tdd-cycles
git push -u entrega fix/modify-url-query-repeated-params
git push -u entrega test/get-dev-env-label
```

A branch `ptoss-2-tdd-cycles` concentra a entrega da atividade. As branches
`fix/modify-url-query-repeated-params` e `test/get-dev-env-label` devem ser
mantidas separadas para abrir Pull Requests limpos no Apache Superset.
