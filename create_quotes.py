from gpt4all import GPT4All
from deep_translator import GoogleTranslator
import argparse
import pandas as pd
from datetime import datetime
import spacy

argParser = argparse.ArgumentParser()
argParser.add_argument("iteration", help="the number of quotes to generate", type=int, default=1)
argParser.add_argument("-fr", "--french", help="activate translation", action="store_true")
argParser.add_argument('-o', '--output', help='stores the quotes on a file for you tu use', action='store_true')
argParser.add_argument('-on', '--outputname', help="if you want to happen a file not named quotes.csv")
argParser.add_argument('-t', '--tags', action='store_true')
argParser.add_argument('-v', '--verbose', action='store_true')
args = argParser.parse_args()

model = GPT4All("gpt4all-falcon-q4_0.gguf")

n_max = 200
n_min = 160
n_max_str = f'in maximum {n_max} words'
n_min_str = f'with {n_min} words minimum'

#print(model.list_models())

if args.outputname != None:
    args.output = True
if args.tags:
    nlp = spacy.load('en_core_web_sm')

if args.output:
    print('your results will be saved')
    try :
        if args.outputname != None:
            df = pd.read_csv(args.outputname)
            print(f'file {args.outputname} was found')
        else:
            df = pd.read_csv('quotes.csv')
            print('results will be stored on default location "quotes.csv"')

    except:
        print('No file input detected')
        df = pd.DataFrame({'quotes':[], 'created_at':[], 'language':[], 'tags':[]})

try:
    for i in range(0, args.iteration):
        print('treating number :', i+1 ,'/', args.iteration, end='\n')
        if args.verbose:
            print('generating', end='\n')
        output = model.generate(f"create an inspirational paragraph {n_max_str} {n_min_str} and 5000 characters max", temp=0.4, top_k=40, top_p=0.4, n_batch=256, max_tokens=4096)
        lang = 'en'

        tags = ''
        if args.tags:
            if args.verbose:
                print('tagging', end='\n')
            tags = str(nlp((output)).ents).replace('(', '').replace(')', '')

        if args.french:
            if args.verbose:
                print('translating', end='\n')
            lang = 'fr'
            output = GoogleTranslator(source='en', target='fr').translate(output)

        if args.output:
            if output not in df.values:
                temp_df = pd.DataFrame({'quotes':[output], 'created_at':[datetime.now()], 'language':[lang], 'tags':[tags]})
                df = pd.concat([df, temp_df], ignore_index=True)
            else:
                print('this was already created')
        
        if args.verbose:
            print('', end='\n')
            print(output, end='\n')
            print('', end='\n')

    if args.output:
        print('saving all results to csv', end='\n')
        if args.outputname != None:
            df.to_csv(args.outputname, index=False)
        else:
            df.to_csv('quotes.csv', index=False)

except:
    print('An unexpected error occured, try again please')