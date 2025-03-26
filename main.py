import streamlit as st
from metapub import PubMedFetcher, MetaPubError
from dotenv import load_dotenv
import re

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o fetcher
fetch = PubMedFetcher()

# Função para validar se o DOI tem o formato correto
def is_valid_doi(doi):
    return bool(re.match(r"^10.\d{4,9}/[-._;()/:A-Z0-9]+$", doi, re.IGNORECASE))

# Função para obter os PMIDs
def get_pmid(dois):
    list_pmid = []

    for doi in dois:
        if not is_valid_doi(doi):
            print(f"Invalid DOI format: {doi}, skipping.")
            continue

        try:
            pmids = fetch.article_by_doi(doi)
            if pmids and hasattr(pmids, 'pmid'):
                list_pmid.append(pmids.pmid)
            else:
                print(f"No PMID found for DOI: {doi}, skipping.")
        except MetaPubError as e:
            print(f"Error fetching PMID for DOI {doi}: {str(e)}")
            continue
    
    print("PubMed extraction done!")

    # Retorna a lista de PMIDs
    return list_pmid

# Interface Streamlit
st.title('PubMed DOI to PMID Fetcher')

# Caixa de texto para inserir DOIs
dois_input = st.text_area("Insira os DOIs (um por linha)", height=200)

# Quando o botão for pressionado
if st.button("Obter PMIDs"):
    # Separar os DOIs em uma lista
    dois_list = [doi.strip() for doi in dois_input.split("\n") if doi.strip()]
    
    if dois_list:
        # Chamar a função get_pmid
        pmids = get_pmid(dois_list)
        
        if pmids:
            # Exibir os PMIDs encontrados
            pmids_string = ', '.join(pmids)  # Lista de PMIDs separada por vírgulas
            st.write("PMIDs encontrados:")
            st.write(pmids_string)  # Exibe os PMIDs como uma string separada por vírgulas
        else:
            st.write("Nenhum PMID encontrado.")
    else:
        st.error("Por favor, insira pelo menos um DOI.")
