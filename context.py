import math
import pickle
import argparse

from tqdm import tqdm
from argparse import RawTextHelpFormatter

SCALE = 100

# Generate contexts from APA and/or ACA graphs
def generate_contexts(combine, similarity, alpha):
	Ap = pickle.load(open('data/apa_' + similarity + '.pkl','rb'))
	Ac = pickle.load(open('data/aca_' + similarity + '.pkl','rb'))

	context_file = open('contexts/context_' + combine + '_' + similarity + '.txt','w')

	# String to hold the entire context
	contexts = ''

	# List of authors
	A = [author for author, author_neighbours in Ac.items()]
	
	print('Generating context...')
	for author in tqdm(A, ncols=100):
		context = ''

		if combine == 'aca':
			author_neighbours = Ac[author]
			
			if similarity == 'cn':
				for author_, w in author_neighbours.items():
					context += (author + ' ' + author_) * w + ' '

			elif similarity in ['jc', 'aa', 'ra']:
				for author_, w in author_neighbours.items():
					w_= math.ceil(w * SCALE)
					context += (author + ' ' + author_) * w_ + ' '
			else:
				raise Exception('Invalid similarity measure: ', similarity)

		elif combine == 'apa':
			author_neighbours = Ap[author]

			if similarity == 'cn':
				for author_, w in author_neighbours.items():
					context += (author + ' ' + author_) * w + ' '

			elif similarity in ['jc', 'aa', 'ra']:
				for author_, w in author_neighbours.items():
					w_= math.ceil(w * SCALE)
					context += (author + ' ' + author_) * w_ + ' '
			else:
				raise Exception('Invalid similarity measure: ', similarity)
		
		elif combine == 'sum':		
			author_neighbours_c = Ac[author]
			author_neighbours_p = Ap[author]

			if similarity == 'cn':
				for author_, w in author_neighbours_c.items():
					w_ = w
					if author_ in author_neighbours_p:
						w_ += author_neighbours_p[author_]
					context += (author + ' ' + author_) * w_ + ' '

			elif similarity in ['jc', 'aa', 'ra']:
				for author_, w in author_neighbours_c.items():
					w_ = w
					if author_ in author_neighbours_p:
						w_ += author_neighbours_p[author_]
					w_= math.ceil(w * SCALE)
					context += (author + ' ' + author_) * w_ + ' '
			else:
				raise Exception('Invalid similarity measure: ', similarity)
		
		elif combine == 'alpha':		
			author_neighbours_c = Ac[author]
			author_neighbours_p = Ap[author]

			if similarity == 'cn':
				for author_, w in author_neighbours_c.items():
					w_ = alpha * w
					if author_ in author_neighbours_p:
						w_ += (1 - alpha) * author_neighbours_p[author_]
					w_= math.ceil(w * SCALE)
					context += (author + ' ' + author_) * w_ + ' '

			elif similarity in ['jc', 'aa', 'ra']:
				for author_, w in author_neighbours_c.items():
					w_ = alpha * w
					if author_ in author_neighbours_p:
						w_ += (1 - alpha) * author_neighbours_p[author_]
					w_= math.ceil(w * SCALE)
					context += (author + ' ' + author_) * w_ + ' '
			else:
				raise Exception('Invalid similarity measure: ', similarity)

		else:
			raise Exception('Invalid combination rule: ', combine)

		contexts += context + '\n'

	context_file.write(contexts)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate contexts from ACA and/or ACA matrices.',
									 formatter_class=RawTextHelpFormatter)
	parser.add_argument('-c','--combine', dest='combine', default='aca',
			    help='Combination of similarity scores from APA and ACA matrices. Choose among aca,apa,sum,alpha. (default: aca)')
	parser.add_argument('-s','--similarity', dest='similarity', default='cn',
			    help='Similarity measure between author nodes. Choose among cn,jc,aa,ra. (default: cn)')
	parser.add_argument('-a','--alpha', dest='alpha', default='0.5',
			    help='Alpha value used in conjunction with alpha combination rule. \nsimilarity = alpha * ACA + (1 - alpha) * APA \nValue between 0 and 1. (default: 0.5)')

	args = parser.parse_args()

	# Generate contexts
	generate_contexts(combine=args.combine, similarity=args.similarity, alpha=float(args.alpha))
