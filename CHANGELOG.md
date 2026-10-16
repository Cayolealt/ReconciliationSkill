# Changelog

## v1.0.1

Correções para quem instala a skill a partir da release.

- **Esquema de terceiro removido do pacote.** O PNG do esquema de Galvão (2020, rev. 2023) não é
  mais distribuído; a cadeia continua descrita em texto em `references/10-cadeia-padrao.md`.
- **Referências a arquivos que não acompanham a skill.** `references/artigos/` passou a ser
  opcional em todo o pacote: a skill consulta os PDFs se o usuário os tiver colocado ali e trabalha
  só com a extração quando a pasta não existe. O esqueleto do código de prática agora aponta para
  `assets/guia_codigo_de_pratica.docx`, que está no pacote.
- **Skill `dataviz` deixou de ser obrigatória.** É usada se estiver disponível; as regras de
  visualização da própria skill bastam sem ela.
- **Diagrama sem `cairosvg`.** Se a biblioteca não estiver instalada, o diagrama sai em SVG com
  um aviso, em vez de falhar.
- **Instalação.** README com o caminho de upload no Claude, provisionamento para organizações e
  Claude Code; `requirements.txt` com as dependências.

## v1.0.0

Primeira versão pública.
