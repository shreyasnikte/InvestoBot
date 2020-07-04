import yfinance as yf
import etfs
import numpy as np
import pandas as pd


def main():
	df_analysis = get_data()
	make_decision()
	print(df_analysis)
	print(df_analysis.shape)

def get_data():

	cols = ["product", "mean_Window", "Open","High", "Low", "Close", "diff_HiLo", "highest", "lowest"]
	df = pd.DataFrame(columns = cols)


	for etf_name, tickr in etfs.list.items():
		product = yf.Ticker(tickr)
		name = product.info['shortName']
#		Get the data for last one year
		hist_raw = product.history(period="1y")	
		hist = hist_raw.drop_duplicates(keep=False)

#		Calculating the difference between High and Low
		hist.loc[:,cols[-3]] = hist.loc[:, cols[3]] - hist.loc[:,cols[4]]

#		Taking mean of last 200, 100, 50, 30, 15, 5 days
		mean_200d = list(hist.loc[hist.index[-200:-1], cols[2:-2]].mean(axis=0).values)
		mean_100d = list(hist.loc[hist.index[-100:-1], cols[2:-2]].mean(axis=0).values)
		mean_50d = list(hist.loc[hist.index[-50:-1], cols[2:-2]].mean(axis=0).values)
		mean_30d = list(hist.loc[hist.index[-30:-1], cols[2:-2]].mean(axis=0).values)
		mean_15d = list(hist.loc[hist.index[-15:-1], cols[2:-2]].mean(axis=0).values)
		mean_5d = list(hist.loc[hist.index[-5:-1], cols[2:-2]].mean(axis=0).values)
		last = list(hist.loc[hist.index[-1], cols[2:-2]].values)

#		Create a dataframe of above values for the given ETF
		data = [mean_200d, mean_100d,mean_50d, mean_30d,mean_15d, mean_5d, last]
		df_2 = pd.DataFrame(data = data, columns = cols[2:-2])

#		Normalizing the difference to compensate for stock appreciation
		df_2.loc[:,cols[-3]] = df_2.loc[:,cols[-3]]/((df_2.loc[:,cols[3]]+df_2.loc[:,cols[4]])/2)

#		Lowest value
		df_2[cols[-1]] = [hist.loc[hist.index[-200:-1], cols[3]].min(axis=0),
					hist.loc[hist.index[-100:-1], cols[4]].min(axis=0),
					hist.loc[hist.index[-50:-1], cols[4]].min(axis=0),
					hist.loc[hist.index[-30:-1], cols[4]].min(axis=0),
					hist.loc[hist.index[-15:-1], cols[4]].min(axis=0),
					hist.loc[hist.index[-5:-1], cols[4]].min(axis=0),
					hist.loc[hist.index[-1], cols[4]]]
#		Highest Value
		df_2[cols[-2]] = [hist.loc[hist.index[-200:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-100:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-50:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-30:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-15:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-5:-1], cols[3]].max(axis=0),
					hist.loc[hist.index[-1], cols[3]]]

#		Name of the ETF
		df_2[cols[0]] = name

#		Different windows of observation
		df_2[cols[1]] = ['200d', '100d', '50d', '30d', '15d', '5d', '1d']
		df = df.append(df_2)

	return df

def make_decision():
	pass
#	Rule based index fund investing guidance system (decreasing priority):

# 	Rule 1: (< 200 day Lowest)		x20 times

#	Rule 2: (< 100 day Lowest)		x10 times

#	Rule 3: (< 50 day Lowest)		x10 times

#	Rule 4: (< 30 day Lowest) && a std related rule		x10 times

#	Rule 5: (<15 day Lowest) && a std related rule		x5 times

#	Rule 6: (<5 day Lowest) && a std related rule		x5 times

# 	Rule 7: (< 200 day Low) && (< 100 day Low) && (< 50 day Low) && (< 30 day Low) && (< 15 day Low) && (< 5 day Low)		x20 times

#       Rule 8: (< 100 day Low) && (< 50 day Low) && (< 30 day Low) && (< 15 day Low) && (< 5 day Low)		x15 times

#       Rule 9: (< 50 day Low) && (< 30 day Low) && (< 15 day Low) && (< 5 day Low)		x10 times

#       Rule 10: (< 30 day Low) && (< 15 day Low) && (< 5 day Low)		x5 times

#       Rule 11: (< 15 day Low) && (< 5 day Low)		x5 times

#       Rule 12: (< 5 day Low)		x5 times

# 	Rule 13: Last Thursday of the month, 11 a.m.






if __name__ == "__main__":
	main()
