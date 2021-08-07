import nltk

def add_to_source(source, item):
    return source + item + " "

def process_content(sample_text):
    try:
        words = nltk.word_tokenize(sample_text)
        tagged = nltk.pos_tag(words)
        
        chunkGram = ('''
            NP: {(<DT>?<JJ>*(<NN>|<NN.>)+<IN>?)+} #Noun Phrase
            VP: {(<MD>*(<VB>|<VB.>)+(<RB>|<RB.>)*)+} #Verb Phrase
            ''')
                
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        
        word_list = chunked.pos()
        
        np_string = "<span style='font-weight: bold; color: blue;'>"
        vp_string = "<span style='font-weight: bold; color: red;'>"
        newString = ""
        
        for i in range(len(word_list)):
            item = word_list[i]
            if item[1] == 'NP':
                np_string = add_to_source(np_string, item[0][0])
                if word_list[i+1][1] != 'NP':
                    np_string = np_string.strip() + '</span>'
                    newString = newString + np_string + " "
                    np_string = "<span style='font-weight: bold; color: blue;'>"
            elif item[1] == 'VP':
                vp_string = add_to_source(vp_string, item[0][0])
                if word_list[i+1][1] != 'VP':
                    vp_string = vp_string.strip() + '</span>'
                    newString = newString + vp_string + " "
                    vp_string = "<span style='font-weight: bold; color: red;'>"
            else:
                newString = newString + item[0][0] + " "
        return newString
        
    except Exception as e:
        print(str(e))