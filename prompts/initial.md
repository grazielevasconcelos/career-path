# Plano de trabalho — career-path

Registro do plano aprovado e executado para construir o plano de carreira de **Graziele Vasconcelos** e publicá-lo como uma página estática no GitHub Pages.

- **Data:** 29/10/2026
- **Repositório:** https://github.com/grazielevasconcelos/career-path
- **Página publicada:** https://grazielevasconcelos.github.io/career-path/
- **Status:** concluído

---

## 1. Objetivo

Transformar o plano de carreira em uma página web visual, somente leitura e de fácil atualização, mantendo o Markdown como fonte única de verdade.

O projeto deveria ser:

- simples de editar e versionar;
- publicado gratuitamente no GitHub Pages;
- sem dependências externas de runtime;
- acessível em desktop e mobile;
- com visual profissional, inspirado no Apple Developer Design.

## 2. Resultado esperado

1. `plan.md` editável, versionado e legível fora da página.
2. Timeline visual em três raias: **NOW**, **NEXT** e **LATER**.
3. Progresso geral e por raia calculado a partir dos itens concluídos.
4. Filtros por tipo e tag, busca textual e alternância de tema.
5. Pipeline de build e deploy automático a cada push na `main`.
6. Documentação suficiente para editar o plano sem conhecer o código.

## 3. Escopo

### 3.1 Conteúdo

- Objetivo profissional: **Platform Engineer / SRE**.
- Framework de horizontes:
  - `NOW`: 0–3 meses;
  - `NEXT`: 3–6 meses;
  - `LATER`: 6–12 meses.
- Front matter com título, nome, cargo, resumo e data de atualização.
- Itens em Markdown com checklist e campos aninhados:
  - `tipo` (obrigatório);
  - `prioridade` (obrigatório: Alta, Média ou Baixa);
  - `link`;
  - `tags`;
  - `prazo` (opcional);
  - `notas`;
  - `evidência`.
- Ausência do campo `status`: a conclusão é definida exclusivamente pelo checkbox `[x]`.
- Prioridades iniciais por fase:
  - `NOW`: Alta;
  - `NEXT`: Média;
  - `LATER`: Baixa.
- Manter os 6 itens originais, seus IDs, links, tags e a ordem do `plan.md`.
- Repositório público, sem dados sensíveis.

### 3.2 Página

- Idioma **PT-BR**.
- Página somente leitura; a edição acontece no `plan.md`.
- Link **Editar plano** apontando para o editor do GitHub.
- Data da última atualização visível.
- Anel de progresso geral no hero.
- Contador e barra de progresso em cada raia.
- Item concluído riscado e com contador atualizado.
- Filtros por tipo e tag, combináveis entre si.
- Busca textual por nome, nota, tag, tipo, prioridade e evidência.
- Estado dos filtros refletido na URL para permitir compartilhar uma visão filtrada.
- Tema claro por padrão e tema escuro com preferência salva no navegador.
- Botão **Imprimir / PDF** com layout de impressão limpo.
- Layout responsivo e navegação por teclado.
- Respeito a `prefers-reduced-motion`.

### 3.3 Visual

- Inspiração no Apple Developer Design.
- Paleta Apple, tipografia do sistema e bastante espaço em branco.
- Nav sticky com blur e borda sutil.
- Hero com nome, cargo e resumo.
- Timeline vertical com linha em gradiente e nós por raia.
- Cards arredondados, sombra leve e borda discreta.
- Gradiente sutil no fundo do hero.
- Densidade confortável, sem excesso de informação.
- Cores das raias:
  - `NOW`: azul `#0071e3`;
  - `NEXT`: índigo `#5e5ce6`;
  - `LATER`: teal `#30b0c7`.

### 3.4 Técnico

- Zero dependências externas de runtime.
- Python 3 com apenas biblioteca padrão para o build.
- HTML, CSS e JavaScript estáticos.
- Build determinístico: `plan.md` → `dist/`.
- Validação automática do Markdown e do HTML gerado.
- Preview local com rebuild ao salvar.
- GitHub Actions para build, validação e deploy no GitHub Pages.
- Nenhum segredo ou token no código ou no repositório.

## 4. Decisões

| Tema | Decisão |
|---|---|
| Arquitetura | `plan.md` → `src/build.py` → `dist/` → GitHub Actions → GitHub Pages |
| Parser | Front matter simples `chave: valor`, sem PyYAML |
| Fonte de verdade | Somente `plan.md`; o HTML é sempre gerado |
| Conclusão | Checkbox `[x]`; sem campo `status` |
| Prioridades | `NOW` = Alta, `NEXT` = Média, `LATER` = Baixa |
| Tema | Claro por padrão, escuro opcional com `localStorage` |
| Página | Somente leitura, com link para editar o Markdown |
| Deploy | GitHub Actions com source “GitHub Actions” no Pages |
| Dependências | Nenhuma biblioteca externa; Python stdlib |
| Estrutura | Sem framework de front-end e sem backend |

## 5. Arquitetura

```text
plan.md
   │
   ▼
src/build.py ──► valida conteúdo e gera HTML
   │
   ▼
dist/ ──► index.html + styles.css + app.js + favicon.svg
   │
   ▼
GitHub Actions ──► make test ──► GitHub Pages
```

### Fluxo do build

1. Ler o front matter e validar os campos obrigatórios.
2. Identificar as raias `NOW`, `NEXT` e `LATER`.
3. Validar itens, campos permitidos, prioridades, IDs duplicados e URLs.
4. Calcular progresso geral e por raia.
5. Substituir os placeholders do template.
6. Copiar CSS, JavaScript e favicon para `dist/`.
7. Validar o HTML gerado com `src/check.py`.
8. Publicar `dist/` no GitHub Pages pelo workflow.

### Estrutura de arquivos

```text
.
├── plan.md                       # fonte única do plano
├── README.md                     # guia de edição e publicação
├── Makefile                      # build, check, test, run e clean
├── src/
│   ├── build.py                  # parser + validação + gerador estático
│   ├── check.py                  # validação do plano e do HTML
│   ├── watch.py                  # preview local com rebuild automático
│   ├── template.html             # estrutura da página
│   ├── styles.css                # visual, temas, responsivo e impressão
│   ├── app.js                    # filtros, busca, URL e tema
│   └── favicon.svg               # ícone da página
├── .github/workflows/pages.yml   # build + deploy no GitHub Pages
└── dist/                         # gerado; não versionado
```

## 6. Plano de execução

### Etapa 1 — Requisitos e definição do escopo

- Levantar objetivo profissional, horizontes e itens iniciais.
- Definir o formato do `plan.md` e os campos aceitos.
- Definir o visual, as cores das raias e o comportamento da página.
- **Entrega:** escopo fechado e decisões registradas.

### Etapa 2 — Modelagem do `plan.md`

- Criar o front matter com os dados do cabeçalho.
- Converter os 6 itens para o formato de checklist com ID e campos aninhados.
- Definir prioridades por fase e preservar links, tags e ordem.
- Incluir um modelo comentado para novos itens.
- **Entrega:** `plan.md` válido e legível.

### Etapa 3 — Build e validação

- Implementar o parser de front matter, raias e itens.
- Validar campos obrigatórios, prioridades, IDs e URLs.
- Gerar o HTML a partir de um template com placeholders.
- Calcular progresso geral e por raia.
- Criar o script de validação do HTML e dos assets.
- **Entrega:** `make test` executando build + validação.

### Etapa 4 — Template e identidade visual

- Montar a estrutura semântica da página.
- Aplicar a paleta Apple, tipografia do sistema e nav sticky com blur.
- Construir o hero, o anel de progresso, a timeline e os cards.
- Implementar tema claro/escuro, responsividade e estilos de impressão.
- **Entrega:** página estática com o visual aprovado.

### Etapa 5 — Interações

- Implementar filtro por tipo.
- Implementar filtro por tag, com seleção múltipla.
- Implementar busca textual sem acentos e sem diferenciar maiúsculas.
- Sincronizar o estado dos filtros com a URL.
- Implementar o toggle de tema com memória.
- Implementar o botão de impressão.
- **Entrega:** filtros, busca, tema e impressão funcionando.

### Etapa 6 — Preview local e documentação

- Criar o preview com rebuild automático ao salvar.
- Adicionar comandos `make build`, `check`, `test`, `run` e `clean`.
- Documentar edição, campos, conclusão de itens, preview e publicação.
- Documentar erros comuns e como corrigi-los.
- **Entrega:** `README.md` e preview local funcionando.

### Etapa 7 — CI/CD e publicação

- Criar o workflow de build e deploy no GitHub Pages.
- Rodar `make test` antes do deploy.
- Publicar o artefato `dist/` com as actions oficiais do GitHub.
- Fazer o push na `main`.
- **Entrega:** workflow concluído com sucesso.

### Etapa 8 — Verificação final

- Confirmar a página publicada com HTTP 200.
- Verificar título, CSS, JavaScript e favicon.
- Conferir os 6 itens nas raias corretas.
- Testar a marcação `[x]`, o riscado, o contador e o anel.
- Testar prioridade inválida e mensagens de erro.
- **Entrega:** página publicada e validada.

## 7. Critérios de aceite

- [x] `plan.md` é a única fonte de verdade.
- [x] O front matter contém título, nome, cargo, resumo e data.
- [x] As raias `NOW`, `NEXT` e `LATER` existem e têm os horizontes corretos.
- [x] Os 6 itens originais foram preservados.
- [x] Cada item tem `tipo` e `prioridade` válidos.
- [x] IDs são únicos e têm três dígitos.
- [x] Links e evidências são validados como URL HTTP(S).
- [x] `[x]` marca o item como concluído, risca o título e atualiza os contadores.
- [x] O anel de progresso reflete o total de concluídos.
- [x] Os filtros por tipo e tag funcionam e se combinam.
- [x] A busca textual ignora acentos e maiúsculas.
- [x] O estado dos filtros fica na URL.
- [x] O tema claro é o padrão e o escuro é salvo no navegador.
- [x] A página é responsiva e navegável por teclado.
- [x] O layout de impressão remove nav, filtros e botões.
- [x] Não há dependências externas de runtime.
- [x] `make test` valida o plano e o HTML gerado.
- [x] O workflow publica `dist/` no GitHub Pages.
- [x] A página publicada responde com HTTP 200 e carrega os assets.
- [x] O repositório é público e não contém dados sensíveis.

## 8. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Markdown malformado quebrar o build | Parser com mensagens de erro e número da linha |
| Item fora da raia ou com campo inválido | Validação de raias, campos e prioridades |
| Link quebrado ou inválido | Validação de esquema e domínio HTTP(S) |
| Duplicação de conteúdo | `plan.md` como fonte única; `dist/` gerado |
| Deploy falhar | `make test` antes do deploy e logs do workflow |
| Página desatualizada | Deploy automático a cada push na `main` |
| Falta de acessibilidade | HTML semântico, `aria-*`, foco visível e `prefers-reduced-motion` |
| Layout ruim no mobile | Breakpoints em 860 px, 620 px e 380 px |
| Escopo crescer demais | Sem backend, login, banco de dados ou edição pela página |
| Dependência de terceiros | Somente Python stdlib e actions oficiais do GitHub |

## 9. Fora de escopo

- Editar o plano diretamente pela página.
- Autenticação, banco de dados ou API.
- Backend, CMS ou painel administrativo.
- Comentários, notificações ou analytics.
- Dependências de front-end ou bibliotecas externas.
- Domínio próprio.
- Múltiplos planos ou múltiplos usuários.

## 10. Conteúdo inicial

| ID | Item | Raia | Tipo | Prioridade | Tags |
|---|---|---|---|---|---|
| 001 | AWS Certified Cloud Practitioner | NOW | Certificação | Alta | cloud, aws, amazon |
| 006 | IA generativa por dentro | NOW | Curso | Alta | ia |
| 003 | Descomplicando o Kubernetes | NOW | Curso | Alta | devops, kubernetes, containers, iac |
| 002 | Microsoft Certified: Azure Fundamentals | NEXT | Certificação | Média | cloud, azure, microsoft |
| 004 | Descomplicando o Terraform | NEXT | Curso | Média | devops, containers, iac |
| 005 | Kubernetes and Cloud Native Associate (KCNA) | LATER | Certificação | Baixa | devops, kubernetes, containers, iac |

## 11. Operação

### Editar o plano

1. Abrir `plan.md`.
2. Adicionar, remover ou alterar itens.
3. Trocar `[ ]` por `[x]` para concluir.
4. Atualizar a data em `atualizado`.
5. Fazer commit e push na `main`.

### Comandos locais

```bash
make test   # build + validação
make run    # preview em http://127.0.0.1:8000
make clean  # remove dist/
```

Se a porta estiver ocupada:

```bash
PORT=8001 make run
```

### Publicação

O workflow `.github/workflows/pages.yml` roda em todo push na `main` e também pode ser disparado manualmente. O Pages está configurado com source **GitHub Actions**.

## 12. Resultado da execução

- `plan.md` com 6 itens e 0 concluídos na entrega.
- `make test` passando.
- Workflow de build e deploy concluído com sucesso.
- Página publicada em https://grazielevasconcelos.github.io/career-path/ com HTTP 200.
- CSS, JavaScript e favicon carregando corretamente.
- Nenhum dado sensível no repositório.
