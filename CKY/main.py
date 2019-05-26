from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/execute",methods=['POST'])
def execute():
    rules = str(request.form['rules']).splitlines()
    sentences = str(request.form['sentence']).split(' ')
    n = len(sentences)
    rules = format_rules(rules)
    outputs = setup_output(rules,sentences)

    outputs = main_execute(rules, sentences, outputs)
    
    return json.dumps(outputs)

def main_execute(rules, sentences, outputs):
    # print(find_rules(rules,['NP','ADJP']))
    n = len(sentences)
    for j in range(1,n):
        for i in range(j-2,-2,-1):
            for k in range(i+1,j):
                for r in outputs[i+1][k]:
                    for r2 in outputs[k+1][j]:
                        for rule in find_rules(rules,[r['grammar'],r2['grammar']]):
                            outputs[i+1][j].append({'grammar':rule['parent'],'pos': f'({i+1},{k+1})({k+1},{j+1})'})
                            
                            #distinct the output[i+1][j]
                            temp = []
                            for o in outputs[i+1][j]:
                                if o not in temp:
                                    temp.append(o)
                            outputs[i+1][j] = temp
    # format outputs before return
    outputs = format_output(outputs,sentences)
    return outputs

def format_output(outputs,sentences):
    res = outputs
    n = len(outputs[0])
    k = 0
    for o in outputs:
        o.insert(0,[{'grammar':k,'pos':''}])
        k += 1
    _temp = []
    _sen = []
    for i in range(n+1):
        _temp.append([{'grammar':i,'pos':''}])
        _sen.append([{'grammar': (i != 0 and sentences[i-1]) or '','pos':''}])
    res.insert(0,_temp)
    res.insert(0,_sen)
    return res


def setup_output(rules,sentences):
    output = []
    n =  len(sentences)
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append('')
        output.append(temp)
    for i in range(n):
        for j in range(n):
            if len(output[i][j]) == 0:
                output[i][j] = []
            if i == j:
                _rules = find_rules(rules,sentences[i])
                for r in _rules:
                    output[i][j].append({'grammar': r['parent'], 'pos': f'({i},{j+1})'})
    
    return output

def find_rules(rules,key):
    output = []
    for r in rules:
        if r['child1'] == key or (r['child1'] == key[0] and r['child2'] == key[1]):
            output.append(r)
    return output

def format_rules(rules):
    _rules = []
    for r in rules:
        r = r.replace('-> ','').split(' ')
        temp = {}
        temp['parent'] = r[0]
        temp['child1'] = r[1]
        if len(r) > 2:
            temp['child2'] = r[2]
        _rules.append(temp)
    return _rules

if __name__ == "__main__":
    app.run(debug=True, port=1996)