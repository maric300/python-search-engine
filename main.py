from ast import parse
import os
from parser_html import Parser
import trie
import time
import graph
import msort
linkovi = []
reci = []
trie_dict = {}
directory = "C:/Microsoft VS Code/FTN/FTN/Alogirtmi/Search Engine/python-2.7.7-docs-html"
parseric = Parser()
directory_dict = {}
best_val = 0
best_wrd = ""
parsed_words_dict = {}
def iterare_through_dir(directory, list_of_edge_lists, edge_list):
    found_a_html = False
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isdir(f):
            iterare_through_dir(f, list_of_edge_lists, edge_list)
        filename_tup = os.path.splitext(filename)
        if filename_tup[1] == ".html":
            found_a_html = True
            if os.path.isfile(f):
                f = f.replace("/", "\\")
                edge_list.clear()
                linkovi, reci = parseric.parse(f)
                parsed_words_dict[f] = reci.copy()
                edge_list.append(f)
                for link in linkovi.copy():
                    edge_list.append(link)
                list_of_edge_lists.append(edge_list.copy())

                curr_trie = trie.Trie()
                index_cnt = 0
                for rec in reci.copy():
                    curr_trie.add(rec, index_cnt)
                    index_cnt += 1
                trie_dict[f] = curr_trie
                linkovi.clear()
                reci.clear()
    if found_a_html == False:
        return False, None, None
    else:
        return True, list_of_edge_lists, edge_list
found_htmls = {}
def search(direktorijum, word, word_count, vertices_dict):
    global best_val
    global best_wrd
    for filename in os.listdir(direktorijum):
        f = os.path.join(direktorijum, filename)
        if os.path.isdir(f):
                new_word_count = search(f, word, 0, vertices_dict)
                word_count += new_word_count
        filename_tup = os.path.splitext(filename)
        if filename_tup[1] == ".html":
            if os.path.isfile(f):
                f = f.replace("/", "\\")
                countme = trie_dict[f].has_word(word)
                word_count += countme[1]
                if countme[1] > 0:
                    link_wrd_count = 0
                    link_count = 0
                    vertex = vertices_dict[f]
                    for i in graf.incident_edges(vertex, False):
                        link_vertex = i.opposite(vertex)
                        key_list = list(vertices_dict.keys())
                        val_list = list(vertices_dict.values())
                        link_index = val_list.index(link_vertex)
                        link = key_list[link_index]
                        temp_count = search_file_link_special(link, word)
                        if temp_count != 0:
                            link_wrd_count += temp_count
                            link_count += 1
                    eval = round(3 * countme[1] +  0.03 * link_wrd_count + 0.2 * link_count)
                    if f not in found_htmls:
                        found_htmls[f] = eval
                    else:
                        num_to_cmp = found_htmls[f]
                        if eval > num_to_cmp:
                            found_htmls[f] = eval
                    if eval > best_val:
                        best_val = eval
                        best_wrd = word
                    
    return word_count

def search_file_link_special(f, wrd):
    if os.path.isfile(f):
        f = f.replace("/", "\\")
        f = f.replace("/", "\\")
        countme = trie_dict[f].has_word(wrd)
        return countme[1]

def operator_search(wrd_list_bad, direktorijum, vertices_dict):
    curr_operator = wrd_list_bad[1]
    wrd_list_operator = [wrd_list_bad[0], wrd_list_bad[2]]
    new_found_htmls = {}
    found_htmls_copy = {}
    if curr_operator == "OR":
        new_found_htmls.clear()
        found_htmls.clear()
        for wrd in wrd_list_operator:
            wrd_count = search(direktorijum, wrd, 0, vertices_dict)
        new_found_htmls = found_htmls.copy()

    elif curr_operator == "AND":
        new_found_htmls.clear()
        found_htmls_copy.clear()
        wrd_count = search(direktorijum, wrd_list_operator[0], 0, vertices_dict)
        found_htmls_copy = found_htmls.copy()
        found_htmls.clear()
        wrd_count = search(direktorijum, wrd_list_operator[1], 0, vertices_dict)
        for key, value in found_htmls_copy.items():
            if key in found_htmls:
                new_found_htmls[key] = value + found_htmls[key]

    elif curr_operator == "NOT":
        new_found_htmls.clear()
        found_htmls_copy.clear()
        wrd_count = search(direktorijum, wrd_list_operator[0], 0, vertices_dict)
        found_htmls_copy = found_htmls.copy()
        found_htmls.clear()
        new_found_htmls = {}
        wrd_count = search(direktorijum, wrd_list_operator[1], 0, vertices_dict)
        for key, value in found_htmls_copy.items():
            if key not in found_htmls:
                new_found_htmls[key] = found_htmls_copy[key]
    if len(new_found_htmls) == 0:
        print("Nema rezultata pretrage.")
    else:
        while True:
            list_cnt = input("Unesite broj rezultata koje zelite da se ispise(1 - 50): ")
            if list_cnt.isnumeric() == True and (int(list_cnt) > 0 and int(list_cnt) < 51):
                sort_html_dict = {}
                sort_html_dict.clear()
                sort_html_dict = sort_dict(new_found_htmls, int(list_cnt))
                first_html = next(iter(sort_html_dict))
                linkovi2, reci2 = parseric.parse(first_html)
                for rec in reci2:
                    if rec.lower() == best_wrd:
                        best_wrd_index = reci2.index(rec)
                        if best_wrd_index > 4:
                            best_wrd_index = best_wrd_index - 5
                        else:
                            best_wrd_index = 0
                        list_to_print = []
                        for i in range(best_wrd_index, best_wrd_index + 10):
                            list_to_print.append(reci2[i])
                        string_to_print = " ".join(list_to_print)
                        print(string_to_print)
                        break
                list_cnt = int(list_cnt)
                cnt = 1
                for i, j in sort_html_dict.items():
                    if cnt == list_cnt + 1:
                        break
                    print(cnt, "|", i, "|" ,j)
                    cnt += 1
                break
            else:
                print("Niste uneli validan broj.")
        found_htmls.clear()
        sort_html_dict.clear()
        new_found_htmls.clear()
        found_htmls_copy.clear()

def sort_dict(dict, limit):
    sorted_dict = {}
    list_of_val = list(dict.values())
    sorted_list = msort.sort(list_of_val)
    sorted_list.reverse()
    key_list = list(dict.keys())
    val_list = list(dict.values())
    cnt = 0
    for item in sorted_list:
        if cnt >= limit:
            break
        position = val_list.index(item)
        sorted_dict[key_list[position]] = item
        val_list[position] = None
        cnt += 1
    return sorted_dict

def change_dir():
    dict_of_vertices = {}
    while True:
        dir_inp = input("Unesite direktorijum: ")
        if dir_inp == "standard":
            dir_inp = "C:/Microsoft VS Code/FTN/FTN/Alogirtmi/Search Engine/python-2.7.7-docs-html"
        if os.path.exists(dir_inp):
            found_a_html, list_of_edge_lists, edge_list = iterare_through_dir(dir_inp, [], [])
            if found_a_html == True:
                dict_of_vertices.clear()
                dict_of_vertices, graf = graph.graph_from_edgelist(list_of_edge_lists)
                return dir_inp, dict_of_vertices, graf
            else:
                print("Ne postoji nijedan html fajl u unetom direktorijumu.")
        else:
            print("Niste uneli validan direktorjium")

def phrase_quick_search(wrd_listara, direktorijum):
    not_a_phrase = False
    return_cnt = 0
    wrd = wrd_listara[0]
    wrd = wrd.lower()
    wrd_indexes = trie_dict[direktorijum].get_index(wrd)
    if wrd_indexes != None:
        reci4 = parsed_words_dict[direktorijum]
        for index in wrd_indexes:
            for j in range(1, len(phrase_wrd_list)):
                if reci4[index + j] != phrase_wrd_list[j]:
                    not_a_phrase = True
                    break
            if not_a_phrase == True:
                not_a_phrase = False
            else:
                return_cnt += 1
    return return_cnt


new_dir, dict_of_vertices, graf = change_dir()
list_of_operators = ["AND", "OR", "NOT"]
while True:
    print("----------------------------------GLAVNI MENI----------------------------------\n\n")
    print("Otvoren direktorijum: " + new_dir + "\n")
    user_inp = input("1. Promena direktorijuma\n2. Unos reci\n3. Izlaz\n")

    if user_inp.isnumeric() != True:
        print("Niste uneli broj.")
    elif user_inp == "1":
        dict_of_vertices.clear()
        trie_dict.clear()
        parsed_words_dict.clear()
        new_dir, dict_of_vertices, graf = change_dir()
    elif user_inp == "2":
        print("\nZa upotrebu logickih operatora obavezno koristiti velika slova ('AND', 'OR', 'NOT')")
        print("Dozvoljena je upotreba logickog operatora samo sa dva operanda. (java AND python)\n")
        print('Ukoliko zelite da pretrazite vise uzastopnih reci, odnosno frazu, koristite ISKLJUCIVO duple navodnike ("The Python Software Foundation")\n')
        print("Ukucajte 'x' za povratak na glavni meni.")
        while True:
            cont = False
            has_operator_searched = False
            wrd_inp = input("Unesite reci: ")
            if wrd_inp.lower() == "x":
                break
            wrd_list = wrd_inp.split(" ")

            if '"' in wrd_inp:
                phrase_found_htmls = {}
                not_a_phrase = False
                wrd_inp = wrd_inp.strip()
                if wrd_inp[0] == '"' and wrd_inp[-1] == '"':
                    phrase_inp = wrd_inp.strip('"')
                    phrase_wrd_list = phrase_inp.split(" ")
                    for i in range(0, len(phrase_wrd_list)):
                        phrase_wrd_list[i] = phrase_wrd_list[i].lower()
                    wrd = phrase_wrd_list[0]
                    for key, value in trie_dict.items():
                        phrases_found_cnt = 0
                        wrd_indexes = value.get_index(wrd)
                        if wrd_indexes != None:
                            reci3 = parsed_words_dict[key]
                            for index in wrd_indexes:
                                for j in range(1, len(phrase_wrd_list)):
                                    if reci3[index + j] != phrase_wrd_list[j]:
                                        not_a_phrase = True
                                        break
                                if not_a_phrase == True:
                                    not_a_phrase = False
                                else:
                                    link_phrase_count = 0
                                    link_count = 0
                                    phrases_found_cnt += 1
                                    vertex = dict_of_vertices[key]
                                    for i in graf.incident_edges(vertex, False):
                                        link_vertex = i.opposite(vertex)
                                        key_list = list(dict_of_vertices.keys())
                                        val_list = list(dict_of_vertices.values())
                                        link_index = val_list.index(link_vertex)
                                        link = key_list[link_index]
                                        temp_count = phrase_quick_search(phrase_wrd_list, link)
                                        if temp_count != 0:
                                            link_count += 1
                                            link_phrase_count += temp_count

                                    eval = round(10 * phrases_found_cnt + 0.05* link_phrase_count + 0.3 * link_count)
                                    phrase_found_htmls[key] =eval
                while True:
                    cont == False
                    if phrase_found_htmls:
                        list_cnt = input("Unesite broj rezultata koje zelite da se ispise(1 - 50): ")
                        if list_cnt.isnumeric() == True and (int(list_cnt) > 0 and int(list_cnt) < 51):
                            sort_html_dict = sort_dict(phrase_found_htmls, int(list_cnt))
                            first_html = next(iter(sort_html_dict))
                            reci2 = parsed_words_dict[first_html]
                            not_a_phrase = False
                            list_to_prnt = []
                            done = False
                            for i in range(0, len(reci2)):
                                if reci2[i] == phrase_wrd_list[0]:
                                    for j in range(1, len(phrase_wrd_list)):
                                        if reci2[i + j] != phrase_wrd_list[j]:
                                            not_a_phrase = True
                                            break
                                    if not_a_phrase == True:
                                        not_a_phrase = False
                                    else:
                                        for k in range(i - 5, i + 5):
                                            list_to_prnt.append(reci2[k])
                                        string_to_print = " ".join(list_to_prnt)
                                        print("_________________________________________________________________")
                                        print(string_to_print)
                                        done = True
                                        break
                                if done == True:
                                    break
                            list_cnt = int(list_cnt)
                            cnt = 1
                            for i, j in sort_html_dict.items():
                                if cnt == list_cnt + 1:
                                    break
                                print(cnt, "|", i, "|" ,j)
                                cnt += 1
                            sort_html_dict.clear()
                            print("_________________________________________________________________")
                            break
                        else:
                            print("Niste uneli validan broj.")
                    else:
                        print("Nema rezultata pretrage.")
                        break

            
                                    

                                    



            elif "OR" in wrd_list or "AND" in wrd_list or "NOT" in wrd_list:
                if (len(wrd_list) == 3 and wrd_list[1] in list_of_operators):
                    operator_search(wrd_list, new_dir, dict_of_vertices)
                    has_operator_searched = True
                    break
                else:
                    print("Niste uneli validnu pretragu.")
            else:
                for wrd in wrd_list:
                    wrd_count = search(new_dir, wrd, 0, dict_of_vertices)

                if len(found_htmls) == 0:
                    print("Nema rezultata pretrage.")
                else:
                    while True:
                        cont == False
                        list_cnt = input("Unesite broj rezultata koje zelite da se ispise(1 - 50): ")
                        if list_cnt.isnumeric() == True and (int(list_cnt) > 0 and int(list_cnt) < 51):
                            sort_html_dict = sort_dict(found_htmls, int(list_cnt))
                            first_html = next(iter(sort_html_dict))
                            linkovi2, reci2 = parseric.parse(first_html)
                            for rec in reci2:
                                if rec.lower() == best_wrd:
                                    best_wrd_index = reci2.index(rec)
                                    if best_wrd_index > 4:
                                        best_wrd_index = best_wrd_index - 5
                                    else:
                                        best_wrd_index = 0
                                    list_to_print = []
                                    for i in range(best_wrd_index, best_wrd_index + 10):
                                        list_to_print.append(reci2[i])
                                    string_to_print = " ".join(list_to_print)
                                    print(string_to_print)
                                    break
                            list_cnt = int(list_cnt)
                            cnt = 1
                            for i, j in sort_html_dict.items():
                                if cnt == list_cnt + 1:
                                    break
                                print(cnt, "|", i, "|" ,j)
                                cnt += 1
                            found_htmls.clear()
                            sort_html_dict.clear()
                            has_operator_searched = True
                            break
                        else:
                            print("Niste uneli validan broj.")
                break
            break
    elif user_inp == "3":
        break
    else:
        print("Niste uneli dati broj.")
