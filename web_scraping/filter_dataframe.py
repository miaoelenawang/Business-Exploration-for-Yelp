# helper funtion to check each row comtain 
def contain_tag(element, Tag_list):
    return any([i in Tag_list for i in element.split(',')])

# filter data frame by tag
def find_by_tag(dataframe, Tag_list):
    # true or false index from helper function
    TF = [contain_tag(i,Tag_list) for i in dataframe['tag']]
    return dataframe.ix[TF,:]

# example usage
find_by_tag(df, d['Chinese']) 

