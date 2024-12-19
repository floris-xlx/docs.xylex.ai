async def remove_duplicates_from_mdx(filepath):
    print(f"Opening file: {filepath}")
    with open(filepath, 'r') as file:
        lines = file.readlines()

    seen_queries = set()
    seen_cards = set()
    unique_lines = []
    skip_line = False

    for line in lines:
        if skip_line:
            print(f"Skipping line: {line.strip()}")
            skip_line = False
            continue

        if 'query="' in line:
            query_start = line.find('query="') + len('query="')
            query_end = line.find('"', query_start)
            query_value = line[query_start:query_end]
            print(f"Found query: {query_value}")

            if query_value in seen_queries:
                print(f"Duplicate query found: {query_value}, skipping line.")
                skip_line = True
                continue
            else:
                seen_queries.add(query_value)
                print(f"Adding query to seen: {query_value}")

        if '<Card title="' in line:
            card_start = line.find('<Card title="') + len('<Card title="')
            card_end = line.find('"', card_start)
            card_value = line[card_start:card_end]
            print(f"Found card title: {card_value}")

            if card_value in seen_cards:
                print(f"Duplicate card title found: {card_value}, skipping line.")
                skip_line = True
                continue
            else:
                seen_cards.add(card_value)
                print(f"Adding card title to seen: {card_value}")

        unique_lines.append(line)

    # Ensure there is an even number of <ParamField and </ParamField> in the file
    open_tags = sum(1 for line in unique_lines if '<ParamField' in line)
    close_tags = sum(1 for line in unique_lines if '</ParamField>' in line)
    
    while close_tags > open_tags and unique_lines and unique_lines[-1].strip() == '</ParamField>':
        print("Removing excess </ParamField> at the end of the file to balance tags.")
        unique_lines.pop()
        close_tags -= 1


    print(f"Writing unique lines back to file: {filepath}")
    with open(filepath, 'w') as file:
        file.writelines(unique_lines)
