## 1. INSTALAÇÃO

Este software requer Python 3 instalado no sistema.
https://www.python.org/downloads/

Rode o arquivo `install.py` para instalar as dependências.

## 2. COMO USAR

O script deve ser rodado com

`python pdf_generator.py [argumentos]`

Os argumentos disponíveis são:

`-t, --template`: Arquivo HTML de template (padrão: `template.html`)
`-d, --data`: Arquivo de dados CSV ou Excel (xls, xlsx, etc)
`-o, --output`: Nome dos arquivos de saída (padrão: `${!i}_out.pdf`)
`-l, --locale`: Locale/idioma utilizado (padrão: `pt-BR`)

### 2.1. SINTAXE

O gerador funciona usando um arquivo HTML como template, que será preenchido por dados.
Será gerado um arquivo PDF para cada conjunto de dados.

O arquivo template é um HTML como qualquer outro, e pode ser customizado como quiser.
Porém, ele possui um adicional:

`${nome_da_coluna}`

Será substituído por um valor na coluna nome_da_coluna do conjunto de dados (linha) atual.
O nome das colunas NÃO É SENSÍVEL A MAIÚSCULAS/MINÚSCULAS. `${nome}` e `${NOME}` se referem à mesma coluna.
Esses são os "campos" dos PDFs resultantes.
Você também pode escrever:

`${nome_da_coluna;<flags>}`

Para adicionar alguma formatação adicional no campo. Atualmente existem as seguintes flags:

`u` - Upper case (TUDO MAIÚSCULO)
`l` - Lower case (tudo minúsculo)
`c` - Capital case (Iniciais Maiúsculas)
`s` - Underlines (Substitui_espaços_por_underlines)
`d` - Datas (formata datas; mais detalhes abaixo)

Você pode combinar as flags. Por exemplo,

`${Nome Completo;su}`

Fará valores da coluna "Nome Completo" aparecerem "MAIÚSCULAS_E_COM_UNDERLINES".

#### 2.1.1 DATAS

A flag de formatação de data requer um parâmetro adicional.

`${alguma_data;d;<formato>}`

Quando você escreve isso, quer dizer que você quer escrever a data da coluna alguma_data
em um formato específico, de acordo com a especificação datetime.strftime.
Isso só funciona se a coluna alguma_data estiver no formato YYYY-mm-dddd.
Por exemplo:

`${nascimento;d;%Y de %B}`

Será substituído por "2022 de junho" se o valor na coluna for exatamente "2022-06-10" (sem aspas).

### 2.2 VALORES ESPECIAIS

Existem alguns nomes de colunas coringas, que serão substituídos por valores especiais.
Todos os nomes coringas começam com um ponto de exclamação (!). Por extensão, nenhuma
coluna de SEUS dados deve começar com um '!'.

Atualmente existem dois valores especiais:

`!i` - Índice atual dos dados, começando pelo 0.
`!date` - Data atual, no formato YYYY-mm-dddd.

Esses valores também podem ser formatados pelas flags de formatação. Por exemplo:

`${!date;sud;%B de %Y}`

Sempre será substituído por MÊS_DE_ANOATUAL. (ex. JUNHO_DE_2022)

### 2.3 NOME DOS ARQUIVOS DE SAÍDA

O nome dos arquivos de saída utiliza exatamente a mesma sintaxe de preenchimento dos arquivos HTML.
Isso quer dizer que você pode especificar algo como

`exemplo_${!i}.pdf`

E os arquivos de saída serão exemplo_0.pdf, exemplo_1.pdf, exemplo_2.pdf, etc.
Note que é possível, então, alguns arquivos terem o mesmo nome. Quando isso acontece, o mais recente
sempre substuirá completamente o mais antigo. Então, mesmo se você tiver 200 linhas na sua planilha,
se o nome dos arquivos de saída for simplesmente "saida.pdf", o resultado será apenas um arquivo.

Por isso, se recomenda utilizar `${!i}` ou alguma coluna que nunca se repete nos nomes.

### 2.4 DADOS

O script utiliza como fonte de dados um arquivo de planilha CSV, Excel ou OpenDocument.
Se você rodar o script sem especificar um arquivo de dados, você deverá inserir os dados manualmente
para uma única entrada pelo terminal, de acordo com o que for especificado no template.

Se o seu template tiver alguma coluna não presente na sua planilha, você deverá inserir manualmente
um valor padrão no terminal. Esse valor padrão será utilizado em todos os PDFs gerados.

## 3. EXEMPLOS

Gera um único PDF. Você deve preencher todos os campos pelo terminal.
`python pdf_generator.py -o saida_unica.pdf`

Gera um PDF para cada linha na planilha pessoas.csv. O nome de cada arquivo será o CPF das pessoas.
`python pdf_generator.py -d pessoas.csv -o '${cpf}.pdf'`

Mostra a data de hoje num formato legível. (23 de maio de 2022)
`${!date;d;%d de %B de %Y}`

Mostra nomes todos maiúsculos.
`${nome;u}`

Gera um PDF para cada linha na planilha plan_topdesk.csv. O nome de cada arquivo será RCBTO_NOTEBOOK_indice_NOME_DA_PESSOA.pdf.
`python pdf_generator.py -d plan_topdesk.csv -o 'RCBTO_NOTEBOOK_${!i}_${Tarefa - Pessoas;su}.pdf'`
