import re
import requests
from bs4 import BeautifulSoup


def clean_snp_refs(snp_reference) -> str:
    """
    Cleans the SNP reference by removing any non-alphanumeric characters and returning only the reference code.
    
    Args:
        snp_reference (str): The SNP reference code.
        
    Returns:
        str: The cleaned SNP reference code.
    """
    # Use regular expressions to remove any non-alphanumeric characters
    str_ref = str(snp_reference)
    cleaned_reference = re.sub(r'\W+', '', str_ref)
    
    return cleaned_reference


def get_snpedia_pages(snp_refs):
    """
    Retrieves the SNPedia pages for the given SNP references.
    
    Args:
        snp_refs (list): A list of SNP references.
        
    Returns:
        list: A list of SNPedia pages as strings. If a page cannot be fetched, None is added to the list.
    """
    pages = []
    for ref in snp_refs:
        try:
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            str_ref = clean_snp_refs(ref)
            url = 'https://www.snpedia.com/index.php/' + str_ref
            session = requests.Session()
            response = session.get(url, headers=headers)
            
            print(response.text)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                body_content = soup.body
                pages.append(str(body_content))
            else:
                pages.append(None)
        except Exception as e:
            print(f"Error fetching SNPedia page for {ref}: {str(e)}")
            pages.append(None)
    return pages


def get_snp_genotypes(snp_refs, pages):
    """
    Retrieves the genotypes associated with the given SNP references.
    
    Args:
        snp_refs (list): A list of SNP references.
        pages (list): A list of SNPedia pages as strings.
        
    Returns:
        list: A list of tuples containing SNP references and their associated genotypes.
    """
    snp_genotypes = []
    for i, page in enumerate(pages):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            gen_table = soup.find('table', class_='sortable')
            if gen_table:
                gen_tds = gen_table.find_all('td')

                genot_list = []
                for gen_td in gen_tds:
                    if gen_td.text.strip():
                        genot_list.append(gen_td.text.strip())
                snp_genotypes.append((snp_refs[i], genot_list))
        except Exception as e:
            print(f"Error getting SNP genotypes for {snp_refs[i]}: {str(e)}")
    return snp_genotypes




def get_snp_articles(snp_refs, pages):
    """
    Retrieves the articles associated with the given SNP references.
    
    Args:
        snp_refs (list): A list of SNP references.
        pages (list): A list of SNPedia pages as strings.
        
    Returns:
        list: A list of tuples containing SNP references and their associated articles.
    """
    snp_articles = []
    for i, page in enumerate(pages):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            articles = soup.find_all(lambda tag: tag.name == 'a' and tag.find_previous_sibling('br') is not None and 'external' in tag.get('class', []) and re.match(r'PMID\s\d+', tag.text))

            articles_list = []
            for article in articles:
                if article.text.strip():
                    articles_list.append(article.text.strip())
            snp_articles.append((snp_refs[i], articles_list))
        except Exception as e:
            print(f"Error getting SNP articles for {snp_refs[i]}: {str(e)}")
    return snp_articles



def get_articles_urls(snp_refs, pages):
    """
    Retrieves the URLs of the articles associated with the given SNP references.
    
    Args:
        snp_refs (list): A list of SNP references.
        pages (list): A list of SNPedia pages as strings.
        
    Returns:
        list: A list of tuples containing SNP references and their associated article URLs.
    """
    link_urls = []
    for i, page in enumerate(pages):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            links = soup.find_all(lambda tag: tag.name == 'a' and tag.find_previous_sibling('br') is not None and 'external' in tag.get('class', []) and re.match(r'PMID\s\d+', tag.text))

            links_list = []
            for link in links:
                url = link.get('href')
                if url:
                    links_list.append(url)
            link_urls.append((snp_refs[i], links_list))
        except Exception as e:
            print(f"Error getting articles URL for {snp_refs[i]}: {str(e)}")
    return link_urls



def get_snp_articles_titles(snp_refs, pages):
    """
    Retrieves the titles of the articles associated with the given SNP references.
    
    Args:
        snp_refs (list): A list of SNP references.
        pages (list): A list of SNPedia pages as strings.
        
    Returns:
        list: A list of tuples containing SNP references and their associated article titles.
    """
    text_after_links = []
    for i, page in enumerate(pages):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            links = soup.find_all(lambda tag: tag.name == 'a' and tag.find_previous_sibling('br') is not None and 'external' in tag.get('class', []) and re.match(r'PMID\s\d+', tag.text))

            links_list = []
            for link in links:
                next_sibling = link.find_next_sibling(text=True)
                if next_sibling:


                    title = next_sibling.text.strip().lstrip(']')  # Remove leading ']'
                    links_list.append(title)
                    #links_list.append(next_sibling.text.strip())

            text_after_links.append((snp_refs[i], links_list))
        except Exception as e:
            print(f"Error getting articles titles for {snp_refs[i]}: {str(e)}")

    return text_after_links


def get_regions_values(snp_refs, pages):
    regions_values = []

    for i, page in enumerate(pages):
        try:
            #pattern = r'var series = (\[[^\]]+\])'
            pattern = r'var series = \[({"data":\[{[\s\S]*)}\]}\];'
            match = re.search(pattern, page)

            data_list = []
            if match:
                for group in match.groups():
                    data_string = group
                    data_list.extend(data_string.split(','))

            # Limpiar los valores (eliminar comillas y espacios)
            clean_data_list = [value.strip().strip('"') for value in data_list]
            regions_values.append((snp_refs[i], clean_data_list))

        except Exception as e:
            print(f"Error getting regions values for {snp_refs[i]}: {str(e)}")

    return regions_values




def get_regions_desc(snp_refs, pages):
    extracted_texts = []

    pattern = r'"meta":"[^"]+\sof\s([^"]+)"'

    for i, page in enumerate(pages):
        try:
            matches = re.finditer(pattern, page)
            for match in matches:
                extracted_texts.append((snp_refs[i], match.group(1)))

        except Exception as e:
            print(f"Error getting regions descriptions for {snp_refs[i]}: {str(e)}")
    return extracted_texts






# def get_snp_regions(snp_refs, pages):
#     snp_regions = []

#     for i, page in enumerate(pages):
#         try:
#             pattern = r'var labels = (\[[^\]]+\])'
#             match = re.search(pattern, page)

#             if match:
#                 data_string = match.group(1)
#                 data_list = data_string.split(',')

#                 # Limpiar los valores (eliminar comillas y espacios)
#                 clean_data_list = [value.strip().strip('"') for value in data_list]

#                 snp_regions.append((snp_refs[i], clean_data_list))
#         except Exception as e:
#             print(f"Error getting SNP regions for {snp_refs[i]}: {str(e)}")

#     return snp_regions



