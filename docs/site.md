# Uso do site

[← Voltar ao README](../README.md)

## Filtros e tema

- Filtro por tipo, por tag e busca textual; os filtros combinam entre si.
- O estado dos filtros fica na URL, então é possível compartilhar uma visão filtrada.
- Tema claro por padrão; o botão de tema alterna para escuro e salva a preferência no navegador.

## Impressão / PDF

O botão **Imprimir / PDF** abre um guia com as opções recomendadas. A impressão
usa o layout A4 retrato do site, com cores, e respeita os filtros e a busca
ativos. No conteúdo atual, o resultado tem cerca de 2 páginas.

- O PDF é sempre claro, mesmo quando a página está no tema escuro.
- Desmarque **Cabeçalhos e rodapés** para remover data, título e URL do navegador.
- Marque **Gráficos de fundo** para manter as cores dos badges, raias e do anel
  de progresso.
- No celular, use a opção **Salvar como PDF**.
- A fonte Inter é empacotada localmente em `src/fonts/` (licença OFL), então o
  PDF embute a mesma fonte em Linux, Android, iOS e macOS.
- O link **Como imprimir** no rodapé reabre o guia. Marque "Não mostrar este
  guia novamente" para abrir a impressão do navegador diretamente nas próximas
  vezes.
- O cabeçalho e o rodapé do navegador não podem ser removidos por CSS; por isso
  o guia orienta a desativá-los.
