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

# PTOSS-2: Artefatos de Entrega

Este documento registra os artefatos do repositório da equipe para a atividade
PTOSS-2. O foco é evidenciar o código utilizado, os testes implementados, a
forma de execução, os relatórios de cobertura e o histórico de commits.

## Pull Requests

| Pull Request | Responsável | Objetivo | Evidência |
| --- | --- | --- | --- |
| `fix(urls): preserve repeated query parameters` | Integrante responsável pelo ciclo de TDD | Corrigir `modify_url_query` para preservar parâmetros repetidos e listas em query strings | Branch limpa para PR oficial: `fix/modify-url-query-repeated-params` |
| `test(version): cover development environment label` | Integrante responsável pelo teste de versionamento | Adicionar teste unitário para `get_dev_env_label` | Branch limpa para PR oficial: `test/get-dev-env-label` |

Links dos PRs oficiais no Apache Superset:

| Pull Request | Link |
| --- | --- |
| `fix(urls): preserve repeated query parameters` | A preencher após abertura |
| `test(version): cover development environment label` | A preencher após abertura |

## Código-Fonte Utilizado

### Artefatos dos PRs

| Arquivo | Função | Papel |
| --- | --- | --- |
| `superset/utils/urls.py` | `modify_url_query` | Código corrigido por TDD |
| `tests/unit_tests/utils/urls_tests.py` | testes de `modify_url_query` | Testes do PR de correção |
| `superset/utils/version.py` | `get_dev_env_label` | Código existente exercitado por teste novo |
| `tests/unit_tests/utils/version_tests.py` | testes de `get_dev_env_label` | Testes do PR de cobertura unitária |

### Artefatos da cobertura agregada da equipe

| Método/função | Módulo usado no `--cov` | Arquivo de teste esperado |
| --- | --- | --- |
| `get_current_user` | `superset.tasks.utils` | `tests/unit_tests/utils/ptoss_unitarios_test.py` |
| `get_dev_env_label` | `superset.utils.version` | `tests/unit_tests/utils/version_tests.py` ou teste equivalente da equipe |
| `user_label` | `superset.utils.core` | `tests/unit_tests/utils/ptoss_unitarios_test.py` |
| `split` | `superset.utils.core` | `tests/unit_tests/utils/ptoss_unitarios_test.py` |
| `check_for_oauth2` | `superset.utils.oauth2` | `tests/unit_tests/utils/ptoss_unitarios_test.py` |
| `ScreenshotCachePayload.should_trigger_task` | `superset.utils.screenshots` | `tests/unit_tests/utils/ptoss_unitarios_test.py` |
| `modify_url_query` | `superset.utils.urls` | `tests/unit_tests/utils/urls_tests.py` |

Quando um integrante substituir ou mover seu teste, a tabela acima deve ser
atualizada com o novo arquivo de teste e o módulo correspondente deve continuar
presente na configuração de cobertura.

## Testes Implementados

| Arquivo | Escopo |
| --- | --- |
| `tests/unit_tests/utils/urls_tests.py` | Testes de `modify_url_query`, incluindo preservação de parâmetros repetidos e serialização de listas |
| `tests/unit_tests/utils/version_tests.py` | Testes de `get_dev_env_label`, incluindo branch/SHA e precedência das variáveis do GitHub |
| `tests/unit_tests/utils/ptoss_unitarios_test.py` | Testes unitários agregados da atividade, cobrindo os métodos selecionados pela equipe |

Testes principais dos PRs:

| Teste | Objetivo |
| --- | --- |
| `test_modify_url_query_preserves_repeated_existing_parameters` | Verifica que `filter=a&filter=b` não é reduzido para apenas um valor |
| `test_modify_url_query_adds_list_values_as_repeated_parameters` | Verifica que listas recebidas em `kwargs` viram parâmetros repetidos |
| `test_get_dev_env_label_formats_branch_and_sha` | Verifica combinações de branch e SHA |
| `test_get_dev_env_label_prefers_github_environment` | Verifica precedência de `GITHUB_HEAD_REF`, `GITHUB_REF_NAME` e `GITHUB_SHA` |

## Instruções de Execução

### Execução local

Com o ambiente de desenvolvimento do Superset configurado:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/ptoss_unitarios_test.py \
  tests/unit_tests/utils/urls_tests.py \
  tests/unit_tests/utils/version_tests.py \
  -q
```

Execução local com cobertura dos módulos analisados:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  -p pytest_cov.plugin \
  --confcutdir=tests/unit_tests/utils \
  tests/unit_tests/utils/ptoss_unitarios_test.py \
  tests/unit_tests/utils/urls_tests.py \
  tests/unit_tests/utils/version_tests.py \
  --cov=superset.tasks.utils \
  --cov=superset.utils.core \
  --cov=superset.utils.oauth2 \
  --cov=superset.utils.screenshots \
  --cov=superset.utils.urls \
  --cov=superset.utils.version \
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

O workflow de cobertura da atividade fica em:

```text
.github/workflows/ptoss-backend-tests.yml
```

Ele executa os testes agregados da equipe e gera o artefato:

```text
ptoss-coverage-reports
```

O artefato contém:

```text
coverage.xml
htmlcov/index.html
```

O workflow também aceita execução manual com listas customizadas de testes e
módulos de cobertura. Assim, se os testes dos integrantes forem movidos para
outros arquivos, basta informar os novos caminhos no campo `test_paths` e manter
os módulos no campo `coverage_modules`.

## Relatórios de Cobertura

A cobertura conjunta deve ser gerada na branch de integração da entrega, onde
todos os testes da equipe estão presentes ao mesmo tempo. O GitHub Actions não
combina testes que vivem em branches diferentes; ele executa apenas o conteúdo
da branch selecionada.

Processo recomendado:

1. Criar ou manter uma branch de integração da entrega.
2. Incorporar nela os testes de todos os integrantes.
3. Conferir a matriz de métodos e módulos deste documento.
4. Executar o workflow `PTOSS Backend Tests`.
5. Baixar o artefato `ptoss-coverage-reports`.
6. Registrar a tabela de cobertura final nesta seção.

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

Essa tabela deve ser substituída pelo resultado final depois que todos os testes
dos integrantes forem integrados na mesma branch de entrega.

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

### Branch de integração da entrega

| Commit | Papel |
| --- | --- |
| `632fea21ec test: add failing tests for repeated URL query params` | Início do TDD para `modify_url_query` |
| `4209369c15 fix: preserve repeated query params in modify_url_query` | Implementação da correção |
| `6969bdf43d refactor: use urlencode doseq for query serialization` | Refatoração mantendo testes aprovados |
| `fe0f9cb453 test: add PTOSS MC/DC unit tests` | Testes unitários adicionais da atividade |
| `c5343d098e ci: add PTOSS backend coverage workflow` | Workflow de execução e cobertura |
| `f74ec5d6d8 test: cover development environment label` | Teste de versionamento incluído na integração |
| `4bc2e14cc3 ci: include version tests in PTOSS workflow` | Inclusão dos testes de versionamento no workflow |
| `docs: simplify PTOSS repository artifacts` | Documentação final dos artefatos da entrega |

## Integração dos Testes da Equipe

Para medir a cobertura de todos juntos, os testes dos integrantes precisam estar
na mesma branch de integração. A forma recomendada é:

```bash
git switch ptoss-2-entrega
git merge --no-ff <branch-do-integrante>
```

ou, se for necessário trazer apenas commits específicos:

```bash
git cherry-pick <commit-do-teste>
```

Depois de integrar os testes, atualizar este documento e executar o workflow de
cobertura. Se um teste novo analisar um módulo que ainda não está no workflow,
adicionar esse módulo ao campo `coverage_modules` na execução manual ou à lista
padrão do workflow.
