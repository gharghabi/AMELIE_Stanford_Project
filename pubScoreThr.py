from Tkinter import *
import requests
import json



def retrieve_pub(pub_map):
	thr =int(scoreThrStr.get())
	global pubScoreData
	pubScoreData = json.loads(pub_map)
	print(pubScoreData[0])
	print(len(pubScoreData))
	for i in range(0, len(pubScoreData)):
		k = 0
		while k < len(pubScoreData[i][1]):
			if pubScoreData[i][1][k][0] < thr :	
				del pubScoreData[i][1][k]
				k -= 1
			k += 1
	json.dumps(pubScoreData)
	pubTxtWidget.delete(1.0, END)
	pubTxtWidget.insert(CURRENT, json.dumps(pubScoreData))

def send_request(gene_list, phenotype_list, *pubScoreData):
	pubResult = requests.post('https://amelie.stanford.edu/api/', verify=False, data={'genes':gene_list,'phenotypes': phenotype_list})
	retrieve_pub(pubResult.text);


def retrieve_input():
    geneText=geneTxtWidget.get("1.0","end-1c")
    phenotypesText=phenotypesTxtWidget.get("1.0","end-1c")
    send_request(geneText, phenotypesText, pubScoreData)
    
def save_result():
	destination='result.json'
	saveFile = open(destination, 'w')
	saveFile.write(json.dumps(pubScoreData))
	saveFile.close()

root = Tk();
geneTxtWidget = Text(root)
geneTxtWidget.grid(row=0, column=0)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

geneTxtWidget.insert(END, 'Candidate genes (Ensembl ID/HGNC name(+ optional "dominant"/"all"); one per line;max. 1000 genes)')
phenotypesTxtWidget = Text(root) 
phenotypesTxtWidget.grid(row=0, column=2)
phenotypesTxtWidget.insert(END, 'Case phenotypes (HPO IDs; max. 1,000 phenotypes;one per line; see HPO Browser)')

pubTxtWidget = Text(root) 
pubTxtWidget.grid(row=0, column=4)
pubTxtWidget.insert(END, "Publication above the specified threshold")

labelwidget= Label(root, text="Threshold score:").grid(column=0, row=1);

scoreThrStr = StringVar()              
scoreThrTxtB = Entry(root, width=12, textvariable=scoreThrStr) 
scoreThrStr.set("55")
scoreThrTxtB.grid(column=0, row=2) 
pubScoreData = []
buttonSubmitt=Button(root, height=1, width=50, text="Submit", 
                    command=lambda: retrieve_input())
buttonSubmitt.grid(row=2, column=2)
buttonSave=Button(root, height=1, width=50, text="Save", 
                    command= lambda: save_result())
buttonSave.grid(row=2, column=4)



root.mainloop() 