import os
from urllib.parse import unquote



def format_query_response_with_sources(response, fallback_response):
    if len(response.get('source_documents', [])) == 0:
        return fallback_response
    answer = response.get('result', '')
    # sources = get_sources_from_response(response)
    # file_names = [unquote(os.path.splitext(os.path.split(source)[1])[0]) for source in sources]
    # sources_text = '\n'.join([f"• <{file_name}|{file_name.split('/')[-1]}>" for file_name in file_names])
    # formatted_response = f"{answer}\n\nI read these:\n{sources_text}"

    # return formatted_response
    return answer

def get_sources_from_response(response):
    sources = []
    for document in response.get('source_documents', []):
        metadata = document.metadata
        source = metadata.get('source')
        if source:
            sources.append(source)
    return list(set(sources))
