import streamlit as st
from metapub import PubMedFetcher
from dotenv import load_dotenv
import re

load_dotenv()

fetch = PubMedFetcher()


def get_pmid(dois):
    list_pmid = []

    for doi in dois:
        try:
            pmids = fetch.article_by_doi(doi)
            if pmids and hasattr(pmids, 'pmid'):
                list_pmid.append(pmids.pmid)
            else:
                print(f"No PMID found for DOI: {doi}, skipping.")
        except Exception as e:
            print(f"Error fetching PMID for DOI {doi}: {str(e)}")
            continue
    
    print("PubMed extraction done!")

    # Retorna a lista de PMIDs
    return list_pmid


st.title('PubMed DOI to PMID Fetcher')

dois_input = st.text_area("Insira os DOIs (um por linha)", height=200)

if st.button("Obter PMIDs"):
    dois_list = [doi.strip() for doi in dois_input.split("\n") if doi.strip()]
    
    if dois_list:
        pmids = get_pmid(dois_list)
        
        if pmids:
            pmids_string = ', '.join(pmids)  
            st.write("PMIDs encontrados:")
            st.write(pmids_string)  
        else:
            st.write("Nenhum PMID encontrado.")
    else:
        st.error("Por favor, insira pelo menos um DOI.")
