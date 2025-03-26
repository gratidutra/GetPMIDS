import streamlit as st
import os
from metapub import PubMedFetcher
from dotenv import load_dotenv

load_dotenv()
_ = os.getenv("NCBI_API_KEY")


fetch = PubMedFetcher()

def get_pmid(dois):
    list_pmid = []  
    
    for doi in dois:
        pmids = fetch.article_by_doi(doi)
        
        if not pmids or not hasattr(pmids, 'pmid'):
            st.warning(f"No pmid found for DOI: {doi}, skipping.")  
            continue 
        
        list_pmid.append(pmids.pmid)
    
    st.success("PubMed extraction done!")
    return list_pmid


st.title('PubMed DOI to PMID Fetcher')


dois_input = st.text_area("Insira os DOIs (um por linha)", height=200)


if st.button("Obter PMIDs"):

    dois_list = [doi.strip() for doi in dois_input.split("\n") if doi.strip()]
    
    if dois_list:
   
        pmids = get_pmid(dois_list)
        
        if pmids:
            st.write("PMIDs encontrados:")
            st.write(pmids)
        else:
            st.write("Nenhum PMID encontrado.")
    else:
        st.error("Por favor, insira pelo menos um DOI.")
