import pandas as pd

def auto_labelling(filename,action_name):
	# import data and action 
	df = pd.read_csv(filename)
	df_label = pd.read_csv(action_name)
	# create a new column for the stop time
	df_label['time_stop'] = df_label['Time(Seconds)'] + df_label['Length(Seconds)']
	# get the index in which the time is between beginning and end time
	i = 0
	ind_list = []
	label_list = []
	for ind, time in enumerate(df[df.columns[0]]):
		for i in range(len(df_label)):
			if time > df_label['Time(Seconds)'][i] and time < df_label['time_stop'][i]:
				ind_list.append(ind)
				label_list.append(df_label['Label(string)'][i])
				break
				
	# select the data based on the index
	
	df_selected = df.loc[ind_list]
	df_selected['label'] = label_list
	

	
	return df_selected
	
if __name__ == '__main__':
	import glob
	raw_filenames = glob.glob("*signal_raw.data")
	processed_filenames = glob.glob("*signal_mean.data")
	labels = glob.glob('*labels.label')


	raw_labelled = [auto_labelling(data_raw,data_label) for data_raw, data_label in zip(raw_filenames,labels)]
	processed_labelled = [auto_labelling(data_processed,data_label) for data_processed, data_label in zip(processed_filenames,labels)]
	df_raw_labelled = pd.concat(raw_labelled)
	df_processed_labelled = pd.concat(processed_labelled)
	df_raw_labelled.to_csv('labelled_raw_data.csv')
	df_processed_labelled.to_csv('labelled_processed_data.csv')
