import nltk
from nltk.corpus import words

class Motives_list:
    def m_list(motives):
        for i in range(len(motives)):
            motives[i] = motives[i].lower()
        modified_list = []
        for motive in motives:
            if " / " in motive:  
                for sub_motive in motive.split(" / "):
                    if sub_motive not in modified_list:  
                        modified_list.append(sub_motive)
            elif "," in motive:  
                for sub_motive in motive.split(", "):
                    if sub_motive not in modified_list:  
                        modified_list.append(sub_motive)
            elif "&" in motive:  
                for sub_motive in motive.split(" & "):
                    if sub_motive not in modified_list:  
                        modified_list.append(sub_motive)
            else:
                if motive not in modified_list:  
                    modified_list.append(motive)
        return modified_list

