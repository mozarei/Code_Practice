from collections import defaultdict

def replace_span(text, start, end, replacement):
    if not 0<=start<=end<=len(text):raise ValueError('Invalid span')
    return text[:start]+replacement+text[end:]


def replace_first(text, old, new):
    if old=='':raise ValueError('old must not be empty')
    return text.replace(old,new,1)


def assemble_text(title, paragraphs):
    if not isinstance(title,str) or not title.strip():raise ValueError('Invalid title')
    if not isinstance(paragraphs,list) or not all(isinstance(p,str) for p in paragraphs):raise ValueError('Invalid paragraphs')
    parts=[p.strip() for p in paragraphs if p.strip()]
    if not parts:raise ValueError('No nonblank paragraphs')
    return title.strip()+'\n'+'\n'.join(parts)
