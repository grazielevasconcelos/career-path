# career-path

Plano de carreira de **Graziele Vasconcelos**, construído com o framework **NOW / NEXT / LATER** e publicado no GitHub Pages.

**Página:** https://grazielevasconcelos.github.io/career-path/

## Como funciona

O [`plan.md`](plan.md) é a única fonte de verdade. Um script em Python (somente biblioteca padrão) lê o Markdown e gera uma timeline estática em `dist/`. O GitHub Actions publica essa pasta no Pages a cada push na `main`.

```text
plan.md  →  src/build.py  →  dist/  →  GitHub Actions  →  GitHub Pages
```

- `NOW`: 0–3 meses
- `NEXT`: 3–6 meses
- `LATER`: 6–12 meses

A página é **somente leitura**: para marcar um item como concluído, edite o `plan.md`. O botão **Editar plano** abre o arquivo direto no editor do GitHub.

## Como editar

### 1. Cabeçalho

```markdown
---
titulo: Plano de Carreira
nome: Graziele Vasconcelos
cargo: Platform Engineer / SRE
resumo: Uma frase curta sobre o objetivo profissional.
atualizado: 2026-10-29
---
```

Atualize `atualizado` sempre que fizer uma mudança relevante. O formato é `AAAA-MM-DD`.

### 2. Itens

Cada item é um checklist com o ID e o nome em negrito, seguido dos campos aninhados:

```markdown
- [ ] **007 · Nome do item**
  - tipo: Curso
  - prioridade: Média
  - prazo: Mar/2027
  - link: https://exemplo.com
  - tags: cloud, kubernetes
  - notas: Critério para considerar o item concluído.
  - evidência: https://link-da-evidencia.com
```

| Campo | Obrigatório | Formato |
|---|---|---|
| `tipo` | Sim | Texto livre: `Certificação`, `Curso`, `Projeto` etc. |
| `prioridade` | Sim | `Alta`, `Média` ou `Baixa` |
| `prazo` | Não | Texto livre: `Dez/2026`, `1º trimestre/2027` etc. |
| `link` | Não | URL `http` ou `https` |
| `tags` | Não | Separadas por vírgula: `cloud, aws, iam` |
| `notas` | Não | Uma linha de texto |
| `evidência` | Não | URL ou texto que comprove a conclusão |

### 3. Concluir um item

Troque `[ ]` por `[x]`:

```markdown
- [x] **001 · AWS Certified Cloud Practitioner**
```

O card fica riscado, o contador geral e o contador da raia são atualizados automaticamente.

### 4. Adicionar um item

1. Escolha a raia (`NOW`, `NEXT` ou `LATER`).
2. Use o próximo ID disponível, com três dígitos.
3. Copie o modelo comentado no fim do `plan.md`.
4. Preencha `tipo` e `prioridade`; os demais campos são opcionais.
5. Atualize a data do front matter.

## Preview local

Requisitos: Python 3.9+ e `make` (opcional).

```bash
make run
```

Abre em `http://127.0.0.1:8000`. O site é reconstruído ao salvar `plan.md` ou os arquivos de `src/`.

Se a porta estiver ocupada, use `PORT=8001 make run`.

Sem `make`:

```bash
python3 src/build.py
python3 -m http.server -d dist 8000
```

Para validar sem subir servidor:

```bash
make test
```

## Publicação

O workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) roda em todo push na `main` e também pode ser disparado manualmente.

Na primeira vez, ative o Pages em **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Depois de qualquer edição:

```bash
git add plan.md
git commit -m "Atualiza plano de carreira"
git push origin main
```

O site é atualizado em alguns minutos.

## Estrutura

```text
.
├── plan.md                       # fonte única do plano
├── README.md
├── Makefile
├── src/
│   ├── build.py                  # parser + gerador estático
│   ├── check.py                  # validação do plano e do HTML
│   ├── watch.py                  # preview com rebuild automático
│   ├── template.html             # estrutura da página
│   ├── styles.css                # visual claro/escuro, timeline e impressão
│   ├── app.js                    # filtros, busca e tema
│   └── favicon.svg
└── .github/workflows/pages.yml
```

`dist/` é gerado localmente e no CI; não é versionado.

## Filtros e tema

- Filtro por tipo, por tag e busca textual; os filtros combinam entre si.
- O estado dos filtros fica na URL, então é possível compartilhar uma visão filtrada.
- Tema claro por padrão; o botão de tema alterna para escuro e salva a preferência no navegador.
- O botão **Imprimir / PDF** usa o layout de impressão, sem nav, filtros ou botões.

## Problemas comuns

| Mensagem | O que fazer |
|---|---|
| `item inválido` | Confira o formato `- [ ] **001 · Nome**` |
| `campo desconhecido` | Use apenas os campos da tabela acima |
| `raia ausente` | Mantenha `## NOW`, `## NEXT` e `## LATER` |
| `ID duplicado` | Cada item precisa de um ID único |
| `prioridade ... deve ser` | Use `Alta`, `Média` ou `Baixa` |
| `não é uma URL http(s) válida` | Corrija o `link` ou a `evidência` |

O build mostra o número da linha com problema no `plan.md`.
