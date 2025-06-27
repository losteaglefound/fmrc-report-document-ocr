import re



async def parse_markdown_and_create_requests(content, start_index=1):
    """
    Parses Markdown content and returns Google Docs API batchUpdate requests
    for formatted insertion from a cleared document (startIndex=1).
    """
    requests = []
    cursor = start_index

    lines = content.split('\n')
    for line in lines:
        bold_spans = []
        italic_spans = []

        # Parse and strip headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        named_style = 'NORMAL_TEXT'
        if heading_match:
            heading_level = len(heading_match.group(1))
            line = heading_match.group(2)
            named_style = f'HEADING_{min(heading_level, 6)}'

        clean_line = ""
        i = 0
        while i < len(line):
            if line[i:i+2] == '**':
                end = line.find('**', i+2)
                if end != -1:
                    start_pos = len(clean_line)
                    clean_line += line[i+2:end]
                    bold_spans.append((start_pos, start_pos + (end - i - 2)))
                    i = end + 2
                    continue
            if line[i] == '*':
                end = line.find('*', i+1)
                if end != -1:
                    start_pos = len(clean_line)
                    clean_line += line[i+1:end]
                    italic_spans.append((start_pos, start_pos + (end - i - 1)))
                    i = end + 1
                    continue
            clean_line += line[i]
            i += 1

        # Insert clean text
        requests.append({
            'insertText': {
                'location': {'index': cursor},
                'text': clean_line + '\n'
            }
        })

        # Apply paragraph style (e.g., heading)
        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': cursor,
                    'endIndex': cursor + len(clean_line)
                },
                'paragraphStyle': {
                    'namedStyleType': named_style
                },
                'fields': 'namedStyleType'
            }
        })

        # Apply bold formatting
        for start, end in bold_spans:
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': cursor + start,
                        'endIndex': cursor + end
                    },
                    'textStyle': {'bold': True},
                    'fields': 'bold'
                }
            })

        # Apply italic formatting
        for start, end in italic_spans:
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': cursor + start,
                        'endIndex': cursor + end
                    },
                    'textStyle': {'italic': True},
                    'fields': 'italic'
                }
            })

        cursor += len(clean_line) + 1  # account for newline

    return requests


async def clear_body(doc):
    """
    This function takes the document ID and 
    return a clear request.
    """
    end_index = doc.get('body').get('content')[-1]['endIndex']
    return [{
        'deleteContentRange': {
            'range': {
                'startIndex': 1,
                'endIndex': end_index - 1
            }
        }
    }]


async def extract_plain_text(doc):
    text = ""
    for elem in doc.get('body').get('content'):
        if 'paragraph' in elem:
            for run in elem['paragraph'].get('elements', []):
                if 'textRun' in run:
                    text += run['textRun'].get('content', '')
    return text
