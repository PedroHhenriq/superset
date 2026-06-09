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

# PTOSS-2: Artefatos dos Pull Requests

Este documento registra os artefatos mantidos nesta branch de entrega. A branch
contém os itens relacionados aos Pull Requests principais, os testes unitários
integrados da equipe e o workflow usado para gerar evidências de execução e
cobertura no fork.

## Pull Requests

| Pull Request | Objetivo | Branch limpa |
| --- | --- | --- |
| `fix(urls): preserve repeated query parameters` | Corrigir `modify_url_query` para preservar parâmetros repetidos e listas em query strings | `fix/modify-url-query-repeated-params` |
| `test(version): cover development environment label` | Adicionar teste unitário para `get_dev_env_label` | `test/get-dev-env-label` |

Links dos PRs oficiais no Apache Superset:

| Pull Request | Link |
| --- | --- |
| `fix(urls): preserve repeated query parameters` | A preencher após abertura |
| `test(version): cover development environment label` | A preencher após abertura |

## Código-Fonte Utilizado

| Arquivo | Função | Papel |
| --- | --- | --- |
| `superset/utils/urls.py` | `modify_url_query` | Código corrigido por TDD |
| `tests/unit_tests/utils/urls_tests.py` | testes de `modify_url_query` | Testes do PR de correção |
| `superset/utils/version.py` | `get_dev_env_label` | Código existente exercitado por teste novo |
| `tests/unit_tests/utils/version_tests.py` | testes de `get_dev_env_label` | Testes do PR de cobertura unitária |
| `superset/tasks/utils.py` | `get_current_user` | Código exercitado por teste da equipe |
| `tests/unit_tests/tasks/test_get_current_user.py` | testes de `get_current_user` | Testes unitários da equipe |
| `superset/utils/core.py` | `split` e `user_label` | Código exercitado por testes da equipe |
| `tests/unit_tests/utils/test_split.py` | testes de `split` | Testes unitários da equipe |
| `tests/unit_tests/utils/user_label_tests.py` | testes de `user_label` | Testes unitários da equipe |
| `superset/utils/oauth2.py` | `check_for_oauth2` | Código exercitado por teste da equipe |
| `tests/unit_tests/utils/oauth2_tests.py` | testes de `check_for_oauth2` | Testes unitários da equipe |
| `superset/utils/screenshots.py` | `ScreenshotCachePayload.should_trigger_task` | Código exercitado por teste da equipe |
| `tests/unit_tests/utils/test_screenshot_cache_fix.py` | testes de screenshots | Testes unitários da equipe |
| `.github/workflows/ptoss-backend-tests.yml` | workflow de CI | Execução dos testes dos PRs com cobertura no fork |

## Testes Implementados

| Teste | Arquivo | Objetivo |
| --- | --- | --- |
| `test_modify_url_query_preserves_repeated_existing_parameters` | `tests/unit_tests/utils/urls_tests.py` | Verifica que parâmetros repetidos existentes, como `filter=a&filter=b`, não são perdidos |
| `test_modify_url_query_adds_list_values_as_repeated_parameters` | `tests/unit_tests/utils/urls_tests.py` | Verifica que valores recebidos como lista são serializados como parâmetros repetidos |
| `test_get_dev_env_label_formats_branch_and_sha` | `tests/unit_tests/utils/version_tests.py` | Verifica combinações de branch e SHA presentes ou ausentes |
| `test_get_dev_env_label_prefers_github_environment` | `tests/unit_tests/utils/version_tests.py` | Verifica precedência das variáveis de ambiente do GitHub sobre valores locais |
| `TestGetCurrentUser` | `tests/unit_tests/tasks/test_get_current_user.py` | Verifica casos de usuário ausente, anônimo, autenticado e nomes de usuário de borda |
| `test_branch_*` e `test_split_*` | `tests/unit_tests/utils/test_split.py` | Verificam casos de caixa-preta e caixa-branca da função `split` |
| `TestUserLabel*` | `tests/unit_tests/utils/user_label_tests.py` | Verifica partições, valores limite e MC/DC de `user_label` |
| `test_check_for_oauth2_*` | `tests/unit_tests/utils/oauth2_tests.py` | Verifica combinações da decisão de disparo do fluxo OAuth2 |
| `test_no_trigger_when_all_conditions_false` | `tests/unit_tests/utils/test_screenshot_cache_fix.py` | Verifica cenário em que nenhuma condição dispara nova tarefa de screenshot |

## Instruções de Execução

### Execução local

Com o ambiente de desenvolvimento do Superset configurado:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/urls_tests.py \
  tests/unit_tests/utils/version_tests.py \
  tests/unit_tests/tasks/test_get_current_user.py \
  tests/unit_tests/utils/test_split.py \
  tests/unit_tests/utils/user_label_tests.py \
  tests/unit_tests/utils/oauth2_tests.py \
  tests/unit_tests/utils/test_screenshot_cache_fix.py \
  -q
```

Execução local com cobertura dos módulos selecionados:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  -p pytest_cov.plugin \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/urls_tests.py \
  tests/unit_tests/utils/version_tests.py \
  tests/unit_tests/tasks/test_get_current_user.py \
  tests/unit_tests/utils/test_split.py \
  tests/unit_tests/utils/user_label_tests.py \
  tests/unit_tests/utils/oauth2_tests.py \
  tests/unit_tests/utils/test_screenshot_cache_fix.py \
  --cov=superset.utils.urls \
  --cov=superset.utils.version \
  --cov=superset.tasks.utils \
  --cov=superset.utils.core \
  --cov=superset.utils.oauth2 \
  --cov=superset.utils.screenshots \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=xml:coverage.xml \
  --cov-report=html:htmlcov
```

Antes de enviar alterações:

```bash
pre-commit run --all-files
```

### Execução no GitHub Actions

O workflow de cobertura fica em:

```text
.github/workflows/ptoss-backend-tests.yml
```

Por padrão, ele executa:

```text
tests/unit_tests/utils/urls_tests.py
tests/unit_tests/utils/version_tests.py
tests/unit_tests/tasks/test_get_current_user.py
tests/unit_tests/utils/test_split.py
tests/unit_tests/utils/user_label_tests.py
tests/unit_tests/utils/oauth2_tests.py
tests/unit_tests/utils/test_screenshot_cache_fix.py
```

E mede cobertura de:

```text
superset.utils.urls
superset.utils.version
superset.tasks.utils
superset.utils.core
superset.utils.oauth2
superset.utils.screenshots
```

O workflow ignora caminhos de teste e módulos de cobertura que ainda não
existirem na branch. Dessa forma, a mesma configuração pode ser usada antes e
depois da integração dos testes dos integrantes.

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
Depois da execução no GitHub Actions, consultar:

1. `Actions`.
2. Workflow `PTOSS Backend Tests`.
3. Execução da branch de entrega.
4. Seção `Summary`, para o log textual de cobertura.
5. Artefato `ptoss-coverage-reports`, para `coverage.xml` e `htmlcov/`.

Resultado da cobertura dos PRs principais e dos testes integrados:

| Arquivo | Stmts | Miss | Branch | BrPart | Cobertura |
| --- | ---: | ---: | ---: | ---: | ---: |
| `superset/utils/urls.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| `superset/utils/version.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| `superset/tasks/utils.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| `superset/utils/core.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| `superset/utils/oauth2.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| `superset/utils/screenshots.py` | A preencher | A preencher | A preencher | A preencher | A preencher |
| Total dos módulos instrumentados | A preencher | A preencher | A preencher | A preencher | A preencher |

Após a execução do workflow, substituir os campos `A preencher` pelos valores
mostrados no `Summary` do GitHub Actions ou no relatório `coverage.xml`.

## Histórico de Commits

### PR `fix(urls): preserve repeated query parameters`

| Commit | Papel |
| --- | --- |
| `f148b2f7af test: add failing tests for repeated URL query params` | Red: testes falhando |
| `4132e0bff6 fix: preserve repeated query params in modify_url_query` | Green: implementação mínima |
| `dac2465266 refactor: use urlencode doseq for query serialization` | Refactor: uso de API da biblioteca padrão |
| `d94d0f3a3e style: format URL tests` | Ajuste de formatação |

### PR `test(version): cover development environment label`

| Commit | Papel |
| --- | --- |
| `27842d3f9c test: cover development environment label` | Teste unitário para `get_dev_env_label` |

### Branch de entrega

| Commit | Papel |
| --- | --- |
| `632fea21ec test: add failing tests for repeated URL query params` | Início do TDD para `modify_url_query` |
| `4209369c15 fix: preserve repeated query params in modify_url_query` | Implementação da correção |
| `6969bdf43d refactor: use urlencode doseq for query serialization` | Refatoração mantendo testes aprovados |
| `f74ec5d6d8 test: cover development environment label` | Teste de versionamento incluído na integração |
| `4bc2e14cc3 ci: include version tests in PTOSS workflow` | Inclusão dos testes de versionamento no workflow |
| `docs: organize PTOSS delivery artifacts` | Documentação dos artefatos dos PRs |

## Cobertura Conjunta da Equipe

Para medir a cobertura de todos juntos, os testes dos integrantes precisam estar
na mesma branch que executa o workflow. As branches remotas identificadas no
fork de entrega são:

| Método/função | Branch remota | Arquivo esperado |
| --- | --- | --- |
| `get_current_user` | `entrega/feat/unit-tests-get-current-user` | `tests/unit_tests/tasks/test_get_current_user.py` |
| `split` | `entrega/test/add-split-unit-tests` | `tests/unit_tests/utils/test_split.py` |
| `user_label` | `entrega/test/add-user-label-tests` | `tests/unit_tests/utils/user_label_tests.py` |
| `check_for_oauth2` | `entrega/test/unit-tests-check-for-oauth2` | `tests/unit_tests/utils/oauth2_tests.py` |
| `ScreenshotCachePayload.should_trigger_task` | `entrega/test/should_trigger_task` | `tests/unit_tests/utils/test_screenshot_cache_fix.py` |

Como algumas branches estão em bases diferentes do repositório, a integração
mais segura é trazer apenas os arquivos/commits de teste necessários, evitando
merge bruto que altere arquivos não relacionados.

Exemplo de campos para execução manual:

```text
test_paths:
tests/unit_tests/utils/urls_tests.py tests/unit_tests/utils/version_tests.py tests/unit_tests/tasks/test_get_current_user.py tests/unit_tests/utils/test_split.py tests/unit_tests/utils/user_label_tests.py tests/unit_tests/utils/oauth2_tests.py tests/unit_tests/utils/test_screenshot_cache_fix.py

coverage_modules:
superset.utils.urls superset.utils.version superset.tasks.utils superset.utils.core superset.utils.oauth2 superset.utils.screenshots
```
