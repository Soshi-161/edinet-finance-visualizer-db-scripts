import zipfile
from io import BytesIO

from bs4 import BeautifulSoup
import pandas as pd

def unzip_edinet_xbrl(xbrl_zip):
    """
    Extract contents from a zipped XBRL document.
    
    Args:
        zipped_document: Bytes-like object containing the zipped XBRL file
        
    Returns:
        dict: A dictionary where keys are file names and values are the contents of the files.
    """
    result = {}
    with zipfile.ZipFile(BytesIO(xbrl_zip)) as zip_ref:
        for file_info in zip_ref.infolist():
            file_name = file_info.filename
            with zip_ref.open(file_name) as file:
                result[file_name] = file.read()
    return result


def parse_xbrl(xbrl_content):
    """
    Parse XBRL content and extract relevant information.
    
    Args:
        xbrl_content: Bytes-like object containing the XBRL content
    
    Returns:
        pandas.DataFrame: DataFrame containing financial data
    """

    try:
        soup = BeautifulSoup(xbrl_content, 'lxml')
    except Exception as e:
        print(f"Error with parser: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
    # For debbugging: print the document type and first 200 characters
    # print(f"Document type: {soup.name}")
    # print(f"First 200 chars: {str(soup)[:200]}")
    
    # 名前空間を考慮して検索
    # 方法1: 複数のタグ名バリエーションを試す
    tag_variations = [
        'ix:nonfraction', 
        'nonfraction',
        'ix\\:nonfraction',  # エスケープされたバージョン
        {'name': 'nonfraction', 'namespace': 'http://www.xbrl.org/2013/inlineXBRL'}
    ]
    
    # すべてのバリエーションで検索
    tags_nonfraction = []
    for tag_var in tag_variations:
        found_tags = soup.find_all(tag_var)
        if found_tags:
            print(f"Found {len(found_tags)} tags with pattern {tag_var}")
            tags_nonfraction.extend(found_tags)
    
    # 方法2: CSSセレクタを使用
    css_tags = soup.select('[name]')  # name属性を持つすべての要素
    if css_tags and not tags_nonfraction:
        print(f"Found {len(css_tags)} tags with name attribute")
        # 最初の5つのタグの名前を表示
        for i, tag in enumerate(css_tags[:5]):
            print(f"Tag {i}: {tag.name}, attrs: {tag.attrs}")
        tags_nonfraction = [tag for tag in css_tags 
                          if 'nonfraction' in tag.name.lower() 
                          or (tag.get('contextref') is not None)]
    
    # 方法3: 再帰的に検索
    if not tags_nonfraction:
        print("Trying recursive search...")
        all_tags = soup.find_all(True)  # すべてのタグを取得
        print(f"Total tags: {len(all_tags)}")
        tags_nonfraction = [tag for tag in all_tags 
                          if ('nonfraction' in str(tag.name).lower()
                             or tag.get('contextref') is not None)]
    
    if not tags_nonfraction:
        print("WARNING: No nonfraction tags found. This could indicate a parsing problem.")
        return pd.DataFrame()
    else:
        print(f"Successfully found {len(tags_nonfraction)} tags")
    
    # 以下は同じ処理を維持
    list_nonfraction = []
    
    for tag in tags_nonfraction:
        try:
            dict_fs = {}
            dict_fs['account_item'] = tag.get('name')
            dict_fs['contextRef'] = tag.get('contextref')
            dict_fs['format'] = tag.get('format')
            dict_fs['decimals'] = tag.get('decimals')
            dict_fs['scale'] = tag.get('scale', '0')  # デフォルト値を提供
            dict_fs['unitRef'] = tag.get('unitRef')
            
            # 残りの処理は同じ
            if tag.get('sign') == '-' and tag.get('xsi:nil') != 'true':
                amount = int(tag.text.replace(',', '')) * -1 * 10 ** int(dict_fs['scale'] or 0)
            elif tag.get('xsi:nil') != 'true' and tag.text.strip():
                amount = int(tag.text.replace(',', '')) * 10 ** int(dict_fs['scale'] or 0)
            else:
                amount = None
            dict_fs['amount'] = amount
            
            list_nonfraction.append(dict_fs)
        except Exception as e:
            print(f"Error processing tag: {e}")
    
    df_nonfraction = pd.DataFrame(list_nonfraction)
    return df_nonfraction


