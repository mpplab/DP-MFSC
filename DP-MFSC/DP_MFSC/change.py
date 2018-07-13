#line = ['1','2','3','4']
fp = open(r"C:\Users\84664\Desktop\test\data\input\msnbc.dat")
f = open(r"C:\Users\84664\Desktop\test\data\input\-1-2msnbc.dat",'w')
lines = fp.readlines()

for line in lines:
	newline = []
	for x in line.strip().split(' '):
		newline.append(x)
		newline.append('-1')
	newline.append('-2')
	f.write(' '.join(newline) + '\n')
f.close()