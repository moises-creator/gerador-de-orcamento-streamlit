import streamlit as st
from fpdf import FPDF
import base64

# Função para gerar PDF com layout mais organizado
def gerar_pdf(prestador, cliente, itens, servicos, outros):
    pdf = FPDF()
    pdf.add_page()
    
    # Adicionar logo
    if prestador['logo']:
        logo_path = 'logo_temp.png'
        with open(logo_path, 'wb') as f:
            f.write(prestador['logo'].getbuffer())
        pdf.image(logo_path, 10, 8, 33)
    
    # Informações do prestador de serviço
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(50, 10)
    pdf.multi_cell(0, 10, f"Eletricista: {prestador['nome']}\nCelular/WhatsApp: {prestador['telefone']}\nE-mail: {prestador['email']}")
    
    pdf.ln(10)

    # Dimensões e posição da borda
    x_start = 10  # Posição X inicial
    y_start = 40  # Posição Y inicial
    width = 190  # Largura total da borda
    height = 40  # Altura total da borda (ajustável com base no conteúdo)

    # Desenha a borda em torno das informações do cliente e do orçamento
    pdf.rect(x_start, y_start, width, height)

    # Informações do cliente e do orçamento
    pdf.set_font('Arial', '', 12)

    # Posições iniciais para o texto
    x_left = 15  # Posição da coluna da esquerda (ajustada para dentro da borda)
    x_right = 105  # Posição da coluna da direita (ajustada para dentro da borda)
    y_position = y_start + 5  # Posição inicial vertical para ambas as colunas, ajustada dentro da borda

    # Coluna 1 (Informações do Cliente)
    pdf.set_xy(x_left, y_position)
    pdf.cell(90, 10, f"Nome do Cliente: {cliente['nome']}", ln=False)

    # Coluna 2 (Informações do Orçamento)
    pdf.set_xy(x_right, y_position)
    pdf.cell(90, 10, f"Data do Orçamento: {outros.get('data_orcamento', 'DD/MM/AAAA')}", ln=False)

    # Próxima linha
    y_position += 10  # Incrementa a posição vertical

    # Coluna 1
    pdf.set_xy(x_left, y_position)
    pdf.cell(90, 10, f"E-mail: {cliente['email']}", ln=False)

    # Coluna 2
    pdf.set_xy(x_right, y_position)
    pdf.cell(90, 10, f"WhatsApp: {cliente['telefone']}", ln=False)

    # Próxima linha
    y_position += 10  # Incrementa a posição vertical

    # Coluna 1
    pdf.set_xy(x_left, y_position)
    pdf.cell(90, 10, f"Telefone: {cliente['telefone']}", ln=False)

    # Coluna 2
    pdf.set_xy(x_right, y_position)
    pdf.cell(90, 10, f"Validade: {outros.get('validade', 'DD/MM/AAAA')}", ln=False)
    pdf.ln()
    pdf.ln()
    
    # Tabela de Itens
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 10, 'Descrição', border=1)
    pdf.cell(30, 10, 'Quantidade', border=1)
    pdf.cell(30, 10, 'Valor Unitário', border=1)
    pdf.cell(30, 10, 'Total', border=1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 10)
    total_produtos = 0
    for item in itens:
        pdf.cell(100, 10, item['descricao'], border=1)
        pdf.cell(30, 10, str(item['quantidade']), border=1)
        pdf.cell(30, 10, f"R${item['valor']:.2f}", border=1)
        total = item['quantidade'] * item['valor']
        pdf.cell(30, 10, f"R${total:.2f}", border=1)
        pdf.ln()
        total_produtos += total
    
    pdf.ln(5)

    # Total dos Produtos
    pdf.rect(x_start, pdf.get_y(), width, 10)  # Add border below the total of products
    pdf.set_font('Arial', 'B', 12)

    pdf.cell(150, 10, "VALOR TOTAL DE PRODUTOS: ", border=1)
    pdf.cell(40, 10, f"R${total_produtos:.2f}", border=1)
    pdf.ln()
    pdf.ln(5)
    
    # Descritivo dos Serviços
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(150, 10, 'Descritivo dos Serviços - Mão de Obra', border=1)
    pdf.cell(40, 10, 'Valor', border=1)
    pdf.ln()

    valor_mao_obra = 0  # Total dos serviços
    for servico in servicos:
        pdf.cell(150, 10, servico['descricao'], border=1)
        pdf.cell(40, 10, f"R${servico['valor']:.2f}", border=1)
        pdf.ln()
        valor_mao_obra += servico['valor']
    
    pdf.ln(5)
    
    # Total da Mão de Obra
    pdf.rect(x_start, pdf.get_y(), width, 10)  # Add border below the total of services
    pdf.cell(0, 10, f"VALOR TOTAL DA MÃO DE OBRA: R${valor_mao_obra:.2f}", ln=True)
    
    pdf.ln(5)
    
    # Total Geral
    total_geral = total_produtos + valor_mao_obra
    pdf.rect(x_start, pdf.get_y(), width, 10)  # Add border below the total of products
    pdf.set_font('Arial', 'B', 12)

    pdf.cell(150, 10, "TOTAL MÃO DE OBRA + PRODUTOS:", border=1)
    pdf.cell(40, 10, f"R${total_geral:.2f}", border=1)
    
    pdf.ln(10)
    
    # Observações
    pdf.rect(x_start, pdf.get_y(), width, 10)  # Add border below the total of products
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 10, f"OBSERVAÇÕES: {outros['observacoes']}")
    
    return pdf.output(dest='S').encode('latin1')

# Função para salvar arquivo PDF
def save_pdf(pdf_content, filename):
    with open(filename, 'wb') as f:
        f.write(pdf_content)

# Função para gerar link de download
def gerar_link_download(pdf_content, filename):
    b64 = base64.b64encode(pdf_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download PDF</a>'
    return href

# Interface Streamlit
st.title('Gerador de Orçamento')

# Dados do Prestador
st.header('Dados do Prestador de Serviço')
prestador = {
    'nome': st.text_input('Nome/Empresa'),
    'email': st.text_input('Email'),
    'telefone': st.text_input('Telefone'),
    'endereco': st.text_input('Endereço'),
    'site': st.text_input('Site'),
    'logo': st.file_uploader('Sua Logo', type=['png', 'jpg', 'jpeg'])
}

# Dados do Cliente
st.header('Dados do Cliente')
cliente = {
    'nome': st.text_input('Nome/Empresa', key='nome_cliente'),
    'email': st.text_input('Email', key='email_cliente'),
    'telefone': st.text_input('Telefone', key='telefone_cliente'),
    'endereco': st.text_input('Endereço', key='endereco_cliente')
}

# Itens do orçamento
st.header('Itens do Orçamento')
itens = []
n_itens = st.number_input('Número de Itens', min_value=1, step=1)

for i in range(n_itens):
    descricao = st.text_input(f'Descrição do Item {i+1}')
    quantidade = st.number_input(f'Quantidade {i+1}', min_value=1, step=1)
    valor = st.number_input(f'Valor {i+1}', min_value=0.0, step=0.01)
    total = quantidade * valor
    itens.append({
        'descricao': descricao,
        'quantidade': quantidade,
        'valor': valor,
        'total': total
    })

# Seção de Serviços (Mão de Obra)
st.header('Serviços (Mão de Obra)')
servicos = []
n_servicos = st.number_input('Número de Serviços', min_value=1, step=1)

for i in range(n_servicos):
    descricao = st.text_input(f'Descrição do Serviço {i+1}', key=f'descricao_servico_{i}')
    valor = st.number_input(f'Valor do Serviço {i+1}', min_value=0.0, step=0.01, key=f'valor_servico_{i}')
    servicos.append({
        'descricao': descricao,
        'valor': valor
    })

# Outros
st.header('Outros')
outros = {
    'observacoes': st.text_area('Observações'),
    'forma_pagamento': st.selectbox(
        'Forma de Pagamento',
        ['À Vista', 'Débito', 'Crédito', 'PIX', 'Carnê']
    ),
    'prazo_entrega': st.text_input('Prazo de Entrega'),
    'data_orcamento': st.date_input('Data do Orçamento'),
    'validade': st.date_input('Validade do Orçamento')
}

# Botão para gerar PDF
if st.button('Gerar PDF'):
    pdf_content = gerar_pdf(prestador, cliente, itens, servicos, outros)
    filename = f"orcamento_{cliente['nome']}.pdf"
    save_pdf(pdf_content, filename)
    st.success('PDF gerado com sucesso!')
    st.markdown(gerar_link_download(pdf_content, filename), unsafe_allow_html=True)

# Botão para enviar por email (seria necessário configurar uma função de envio por email)
