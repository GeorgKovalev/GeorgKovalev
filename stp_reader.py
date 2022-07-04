def stp_reader(file_name):
    file = open(file_name, "r")

    file_text = file.readlines()
    file_text_without_blank_lines = []
    for line in file_text:
        if line.strip() != "":
            file_text_without_blank_lines.append(line)
    file_text = file_text_without_blank_lines

    start_pos = -1
    for i in range(len(file_text)):
        if file_text[i].lower() == 'section graph\n':
            start_pos = i
            break
        
    if start_pos == -1:
        print("ERROR!")

    cur_pos = start_pos + 1
    edges = []
    arcs = []
    node_count = 0

    while file_text[cur_pos].lower().startswith( ('nodes', 'edges', 'arcs') ):
        if file_text[cur_pos].lower().startswith('nodes'):
            node_count = int(file_text[cur_pos].split()[1])
        cur_pos += 1

    while not file_text[cur_pos].lower().startswith('end'):
        if file_text[cur_pos][0].lower() == 'e':
            edges.append(file_text[cur_pos].split()[1:])
        elif file_text[cur_pos][0].lower() == 'a':
            arcs.append(file_text[cur_pos].split()[1:])

        cur_pos += 1

    file.close()

    return [edges, arcs, node_count]