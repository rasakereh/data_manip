import os.path
import numpy as np

DATA_DIR = "../Data/tropopause/"
OUT_DIR = "../Output/"

YEAR_COUNT = 39
CITIES_COUNT = 167241
FIRST_YEAR = 1979
BIAS_COUNT = 4
BQ = int(24 / BIAS_COUNT)

task_a = np.zeros((BIAS_COUNT, CITIES_COUNT, YEAR_COUNT))
task_b = np.zeros((BIAS_COUNT, CITIES_COUNT, 12))
task_c = np.zeros((CITIES_COUNT, YEAR_COUNT))

for curr_m in range(1, 13):
	for curr_y in range(YEAR_COUNT):
		FILE_PATH = DATA_DIR + str(FIRST_YEAR+curr_y) + str(curr_m).zfill(2) + ".txt"
		if not os.path.exists(FILE_PATH):
			print("Not found:", FILE_PATH)
		else:
			print("opening:", FILE_PATH)
			curr_m_data = np.loadtxt(FILE_PATH)
			days = curr_m_data.shape[1]>>2
		for bias in range(BIAS_COUNT):
			task_a[bias, :, curr_y] = curr_m_data[:, [(i<<2)+bias for i in range(days)]].sum(axis=1)/days
		task_c[:, curr_y] = curr_m_data.sum(axis=1)/(days<<2)
	for bias in range(BIAS_COUNT):
		OUT_PATH = OUT_DIR + "taskA_" + str(curr_m).zfill(2) + "_" + str(bias*BQ).zfill(2) + ".txt"
		print("writing:", OUT_PATH, end='\t')
		np.savetxt(OUT_PATH, task_a[bias], fmt="%.1f", delimiter='\t')
		print("done")
	task_b[:, :, curr_m-1] = task_a.sum(axis=2)/YEAR_COUNT
	OUT_PATH = OUT_DIR + "taskC_" + str(curr_m).zfill(2) + ".txt"
	print("writing:", OUT_PATH, end='\t')
	np.savetxt(OUT_PATH, task_c, fmt="%.1f", delimiter='\t')
	print("done")
for bias in range(BIAS_COUNT):
	OUT_PATH = OUT_DIR + "taskB_" + str(bias*BQ).zfill(2) + ".txt"
	print("writing:", OUT_PATH, end='\t')
	np.savetxt(OUT_PATH, task_b[bias], fmt="%.1f", delimiter='\t')
	print("done")
	
