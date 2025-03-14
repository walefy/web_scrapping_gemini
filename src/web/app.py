import streamlit as st
import json
import os


def load_articles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        articles = json.load(file)
    return articles


def main():
    st.title('Resumo do TabNews')

    json_path = 'output/report.json'

    if not os.path.exists(json_path):
        st.error('O arquivo JSON com os artigos não foi encontrado.')
        return

    articles = load_articles(json_path)

    for article in articles:
        st.header(article['title'])
        st.markdown(f"[Link para o artigo completo]({article['link']})")
        if 'audio_path' in article and article['audio_path']:
            if os.path.exists(article['audio_path']):
                st.audio(article['audio_path'], format='audio/mp3')
            else:
                st.warning('Arquivo de áudio não encontrado.')
        else:
            st.warning('Resumo em áudio não disponível.')


if __name__ == '__main__':
    main()
