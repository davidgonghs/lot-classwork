# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 19:11:45 2020
Week 8 Lab for IoT Module
Topic: Sensor data fusion using KNN
@author: Raz
"""

#### PART One: Data Exploration ##############

# Import necessary packages 

from glob import glob
import pandas as pd

# Activity dataset folder
data_dir = "dataset_activity/"

# Load all the data using 
# Read the each data file's full path and form a list
all_data = glob(data_dir + "*.csv")

# Have a look at the first three paths of the list
all_data[:3]

# Define a function to load the data using previously formed list of files paths

def load_dataset(all_data):
    subjects = pd.DataFrame()
    for i,name in enumerate(all_data):
        df = pd.read_csv(name, header=None)
        df['subject_id'] = i+1
        subjects = subjects.append(df.iloc[:,1:])
    return subjects

# Call the function to the all_data list
subjects_df = load_dataset(all_data)

# Name the columns
subjects_df.columns = ['x', 'y', 'z', 'label','subject_id']
subjects_df.head() # load 
subjects_df.tail()

# Check the total number of subjects 
print('Loaded %d subjects' % len(subjects_df.subject_id.unique()))

# Plot one subject's activity data to explore

from matplotlib import pyplot
#plot the x, y, z acceleration and activities for a single subject

def plot_subject(subject):
    pyplot.figure()
#create a plot for each column
    for col in range(subject.shape[1]):
        pyplot.subplot(subject.shape[1], 1, col+1) # define the subplot size (rows, columns, graphs_no)
        pyplot.plot(subject[:,col])
        pyplot.show()

#plot activities for a single subject
plot_subject(subjects_df[subjects_df.subject_id==1].iloc[:,:4].values)

"""
Discussion on the suject's activity figure:
Running the example creates a line plot for each variable for the first loaded subject. 
We can see some very large movement in the beginning of the sequence that may be an outlier
 or unusual behaviour that could be removed. We can also see that the subject performed 
 some actions multiple times. For example, a closer look at the plot of the class variable
 (bottom plot) suggests the subject performed activities in the following order,
 1, 2, 0, 3, 0, 4, 3, 5, 3, 6, 7. Note that activity 3 was performed twice.
"""

### Plot the total duration

subjects = []

for k,values in subjects_df.groupby('subject_id'):
    subjects.append(values.iloc[:,:4].values)

# returns a list of dict, where each dict has one sequence per activity
def group_by_activity(subjects, activities):
    grouped = [{a:s[s[:,-1]==a] for a in activities} for s in subjects]
    return grouped
# calculate total duration in sec for each activity per subject and plot
def calculate_durations(grouped, activities):
# calculate the lengths for each activity for each subject
    freq = 52
    durations = [[len(s[a])/freq for s in grouped] for a in activities]
    return durations

def plot_durations(grouped, activities):
    durations = calculate_durations(grouped, activities)
    pyplot.boxplot(durations, labels=activities)
    pyplot.show()
    
# grouped
activities = [i for i in range(0,8)]
grouped = group_by_activity(subjects, activities)
# plot durations
plot_durations(grouped, activities)

#############
# Call the calculate_durations function
calculate_durations(grouped, activities)

"""
Discussion about the activties' duration of the subject:
We can see that there is relatively fewer observations for activities 
0 (no activity), 2 (standing up, walking and going up/down stairs), 5 (going up/down stairs) 
and 6 (walking and talking). We can also see that each subject spent a lot of time on activity 
1 (standing Up, walking and going up/down stairs) and activity 7 (talking while standing).


"""

#plot the x, y, z acceleration for each subject
def plot_subjects(subjects):
    pyplot.figure()
#create a plot for each subject
    x_axis = None
    for i in range(len(subjects)):
        ax = pyplot.subplot(len(subjects), 1, i+1, sharex=x_axis)
        if i == 0:
            x_axis = ax
            #plot a histogram of x data
        for j in range(subjects[i].shape[1]-1):
            pyplot.hist(subjects[i][:,j], bins=100)
    #pyplot.show()
            
plot_subjects(subjects)

"""
Discussion of the figure:
    
Running the example creates a single figure with 15 plots, one for each subject, and 3 histograms on each plot for each of the 
3 axis of accelerometer data. The three colors blue, orange and green represent the x, y and z axes. This plot suggests that the
 distribution of each axis of accelerometer is Gaussian or really close to Gaussian. This may help with simple outlier detection
 and removal along each axis of the accelerometer data. The plot really helps to show both the relationship between the 
 distributions within a subject and differences in the distributions between the subjects.
Within each subject, a common pattern is for the x (blue) and z (green) are grouped together to the left and y data (orange) is 
separate to the right. The distribution of y is often sharper whereas the distributions of x and z are flatter.
Across subjects, we can see a general clustering of values around 2,000 (whatever the units are), although with a lot of spread.
 This marked difference in distributions does suggest the need to at least standardize (shift to zero mean and unit variance) 
 the data per axis and per subject before any cross-subject modeling is performed.
"""

####### PART Two: KNN-based activity classification ##############

# Define the variables
X = subjects_df[['x','y','z']]
y = subjects_df['label']

#evaluate the model by splitting into train and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=12)

##Import the Classifier.
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
##Instantiate the model with 5 neighbors.
model = KNeighborsClassifier(n_neighbors=5)
##Fit the model on the training data.
model.fit(X_train, y_train)

#use the model to make predictions with the test data
y_pred = model.predict(X_test)
#how did our model perform?
count_misclassified = (y_test != y_pred).sum()
print('Misclassified samples: {}'.format(count_misclassified))
accuracy = metrics.accuracy_score(y_test, y_pred)
print('Accuracy: {:.2f}'.format(accuracy))

#How to decide the value of n-neighbors
#Choosing a large value of K will lead to greater amount of execution time & under-fitting. 
#Selecting the small value of K will lead to over-fitting. There is no such guaranteed way to find the best value of K.

from sklearn.metrics import accuracy_score
accuracy = []
for K in range(25):
    K_value = K+1
    neigh = KNeighborsClassifier(n_neighbors = K_value)
    neigh.fit(X_train, y_train)
    y_pred = neigh.predict(X_test)
    accuracy.append(accuracy_score(y_test,y_pred)*100)
    print("Accuracy is ", accuracy_score(y_test,y_pred)*100,"% for K-Value:",K_value)


