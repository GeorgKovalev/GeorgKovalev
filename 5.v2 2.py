def stp_reader(file_name):
    file = open(file_name, "r")

    file_text = file.readlines()
    start_pos = -1
    for i in range(len(file_text)):
        if file_text[i] == 'SECTION Graph\n':
            start_pos = i
            break
        
    if start_pos == -1:
        print("ERROR!")

    cur_pos = start_pos + 1
    edges = []
    arcs = []
    node_count = 0

    while file_text[cur_pos].startswith( ('Nodes', 'Edges', 'Arcs') ):
        if file_text[cur_pos].startswith('Nodes'):
            node_count = int(file_text[cur_pos].split()[1])
        cur_pos += 1

    while not file_text[cur_pos].lower().startswith('end'):
        if file_text[cur_pos][0] == 'E':
            edges.append(file_text[cur_pos].split()[1:])
        elif file_text[cur_pos][0] == 'A':
            arcs.append(file_text[cur_pos].split()[1:])

        cur_pos += 1

    print(f'Node count: {node_count}')
    print("Edges:")
    for edge in edges:
        print(edge)
    for arc in arcs:
        print(arc)
    file.close()

    return [edges, arcs]

stp_reader('b18.stp')
