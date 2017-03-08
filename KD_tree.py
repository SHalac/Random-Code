from random import randint

nodes_visited =0;

class KD_Tree():



	# data is a list of lists (each sublist is a data point with K dimensions)
	def __init__(self,data,total_dim,dim=0):
		if(len(data)):
			self.dimension = dim % total_dim
			#print("DIMENSION: %d \n\n" % self.dimension)
			sorted_list = sorted(data, key=lambda x: int(x[self.dimension]))
			median_index = len(sorted_list)//2
			self.root = sorted_list[median_index]

			if(len(data)>2):
				self.LEFT_subtree = KD_Tree(sorted_list[:median_index],total_dim,dim+1)
				self.RIGHT_subtree = KD_Tree(sorted_list[median_index+1:],total_dim,dim+1)
			elif (len(data)==2):
				self.LEFT_subtree = KD_Tree(sorted_list[:median_index],total_dim,dim+1)
				self.RIGHT_subtree = None
			else:
				self.RIGHT_subtree = None
				self.LEFT_subtree = None

		else:
			self.dimension = dim 
			self.root = None 
			self.LEFT_subtree = None
			self.RIGHT_subtree = None

def nearestNeighborSearch(tree,search_point,total_dim,nearestNeighbor = None):
	if(tree):
		global nodes_visited
		nodes_visited += 1
		if nearestNeighbor == None:
			nearestNeighbor = tree.root

			# check the corresponding subtree 
		if tree.root[tree.dimension] > search_point[tree.dimension]:
			nearestNeighbor = nearestNeighborSearch(tree.LEFT_subtree,search_point,total_dim,nearestNeighbor)
						# check if the current node might be better
			if EuclidDistance(tree.root,search_point,total_dim)<EuclidDistance(nearestNeighbor,search_point,total_dim):
				nearestNeighbor = tree.root

			#check if the "far subtree" is worth a look. Distance between splitting coordinate and search point vs curr NN
			hyper_point = list(search_point)
			hyper_point[tree.dimension] = tree.root[tree.dimension]
			if EuclidDistance(hyper_point,search_point,total_dim) < EuclidDistance(nearestNeighbor,search_point,total_dim):
				nearestNeighbor = nearestNeighborSearch(tree.RIGHT_subtree,search_point,total_dim,nearestNeighbor)


		else:
			nearestNeighbor = nearestNeighborSearch(tree.RIGHT_subtree,search_point,total_dim,nearestNeighbor)

			#check if current node is better
			if EuclidDistance(tree.root,search_point,total_dim)<EuclidDistance(nearestNeighbor,search_point,total_dim):
				nearestNeighbor = tree.root

			#check if the "far subtree" is worth a look. Distance between splitting coordinate and search point vs curr NN
			hyper_point = list(search_point)
			hyper_point[tree.dimension] = tree.root[tree.dimension]
			if EuclidDistance(hyper_point,search_point,total_dim) < EuclidDistance(nearestNeighbor,search_point,total_dim):
				nearestNeighbor = nearestNeighborSearch(tree.LEFT_subtree,search_point,total_dim,nearestNeighbor)



		return nearestNeighbor
	return nearestNeighbor


def EuclidDistance(a,b,D):
	sum = 0
	for x in range(len(a)):
		sum += (a[x]-b[x])**2 	
	return sum



if __name__ == '__main__':
	data_dim = input("How many dimensions for the data?\n")
	data_dim = int(data_dim)
	data_size = input("how many data points do you want?\n")
	data_size = int(data_size)
	raw_data = [[randint(0,15) for x in range(data_dim)] for y in range(data_size)]
	print("here is the list that has been created\n")
	print(raw_data)
	myDataTree = KD_Tree(raw_data,data_dim)
	print("Enter a data point to search for :\n")
	point = [int(x) for x in input().split(',')]
	print(point)
	neighbor = nearestNeighborSearch(myDataTree,point,data_dim)
	print("______NEAREST NEIGHBOR SEARCH RESULT:")
	print(neighbor)
	print("_______%___OF NODES VISITED______")
	print(	float(nodes_visited)/float(len(raw_data)) )

		



