g_word_list = list()
g_sentence_list = list()
g_length = list()
g_punct = ['.',';',':','-','?','!',',','"',"'",'(',')']
g_longest = 0
g_shortest = 0

def search(p_x):
    global g_word_list
    global g_shortest
    global g_longest
    global g_punct

    p_list_sub = list()
    for i in g_punct:
        n = 0
        while i in p_x[n:]:
            if i == "'":
                if p_x[p_x.index(i)-1] == 'e':
                    pass
                else:
                    pos = p_x.index(i,n)
            else:
                pos = p_x.index(i,n)
                if pos < len(p_x)-2:
                    if p_x[pos] != ',' or p_x[pos+2] != '0':
                        p_list_sub.append([pos, p_x[pos]])
                else:
                    p_list_sub.append([pos, p_x[pos]])
            n = pos + 1

    p_list_sub2 = list()
    m = 0
    while m < len(p_x):
        in_list = False
        if len(p_x) - m -1 < g_longest:
            L = len(p_x) - m
        else:
            L = g_longest
        for i in range(g_shortest,L+1):
            if p_x[m:m+i].lower() in g_word_list:
                in_list = True
                w = p_x[m:m+i]
        if in_list == True:
            p_list_sub2.append([m, w])
            m += len(w)
        else:
            m += 1

    return p_list_sub, p_list_sub2

def combine(p_x):
    global g_sentence_list
    global g_punct

    line = ''
    l1, l2  = search(p_x)
    l3 = l1 + l2
    l = sorted(l3)
    s = ''
    for i in l:
        s += i[1]
    if s in g_sentence_list:
        for i in range(len(l)-1):
            if l[i][1] in ['-']:
                line += l[i][1]
            elif l[i][1] in ['(']:
                line += ' ' + l[i][1]
            elif l[i][1] in ['"',"'"] or l[i+1][1] in g_punct:
                line += l[i][1]
            else:
                line += l[i][1] + ' '
        line += l[-1][1]
    else:
        line = s
    return line    

def main():
    global g_word_list
    global b_list
    global g_sentence_list
    global g_length
    global g_longest
    global g_shortest

    with open('word.txt','r') as f:
        for word in f:
            word = word.strip('\n')
            if word[-1] == '0':
                if len(word) == 4:
                    word = word[0]+','+word[1]+word[2]+word[3]
                elif len(word) == 5:
                    word = word[0]+word[1]+','+word[2]+word[3]+word[4]
            g_word_list.append(word)

    with open('sentence.txt','r') as fr:
        for l in fr:
            l = l.strip('\n')
            g_sentence_list.append(l)

    for i in g_word_list:
        j = len(i)
        g_length.append(j)
    g_longest = sorted(g_length)[-1]
    g_shortest = sorted(g_length)[0]

    output = open('output.txt','w')
    for i in g_sentence_list:
        output.write(combine(i)+'\n')
    output.close()

if __name__ == '__main__':
    main()