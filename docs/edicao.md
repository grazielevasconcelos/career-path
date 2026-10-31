# Como editar o plano

[← Voltar ao README](../README.md)

O [`career.md`](../career.md) é a fonte única de verdade.

## Cabeçalho

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

## Itens

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

## Campos

| Campo | Obrigatório | Formato |
|---|---|---|
| `tipo` | Sim | Texto livre: `Certificação`, `Curso`, `Projeto` etc. |
| `prioridade` | Sim | `Alta`, `Média` ou `Baixa` |
| `prazo` | Não | Texto livre: `Dez/2026`, `1º trimestre/2027` etc. |
| `link` | Não | URL `http` ou `https` |
| `tags` | Não | Separadas por vírgula: `cloud, aws, iam` |
| `notas` | Não | Uma linha de texto |
| `evidência` | Não | URL ou texto que comprove a conclusão |

## Concluir um item

Troque `[ ]` por `[x]`:

```markdown
- [x] **001 · AWS Certified Cloud Practitioner**
```

O card fica riscado, o contador geral e o contador da raia são atualizados automaticamente.

## Adicionar um item

1. Escolha a raia (`NOW`, `NEXT` ou `LATER`).
2. Use o próximo ID disponível, com três dígitos.
3. Copie o modelo comentado no fim do `career.md`.
4. Preencha `tipo` e `prioridade`; os demais campos são opcionais.
5. Atualize a data do front matter.

## Problemas comuns

| Mensagem | O que fazer |
|---|---|
| `item inválido` | Confira o formato `- [ ] **001 · Nome**` |
| `campo desconhecido` | Use apenas os campos da tabela acima |
| `raia ausente` | Mantenha `## NOW`, `## NEXT` e `## LATER` |
| `ID duplicado` | Cada item precisa de um ID único |
| `prioridade ... deve ser` | Use `Alta`, `Média` ou `Baixa` |
| `não é uma URL http(s) válida` | Corrija o `link` ou a `evidência` |

O build mostra o número da linha com problema no `career.md`.
