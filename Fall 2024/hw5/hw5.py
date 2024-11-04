# add your code to this file
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

def clean_data(filepath):
    df = pd.read_csv(os.path.join(filepath))
    df = df.dropna(subset=['Days of Ice Cover'])
    df["Winter"] = df['Winter'].str[:4].astype(int)
    df["Days of Ice Cover"] = df["Days of Ice Cover"].astype(int)
    filtered = df.loc[(df['Winter'] >= 1855) & (df['Winter'] <= 2022)]
    filtered = filtered[['Winter', 'Days of Ice Cover']]
    filtered = filtered.rename(columns={'Winter': 'year', 'Days of Ice Cover': 'days'})
    filtered.to_csv('hw5.csv', index=False) 

def vis(filename):
    df = pd.read_csv(os.path.join(filename))
    plt.plot(df['year'], df['days'])
    plt.xlabel('Year')
    plt.ylabel('Number of Ice-Covered Days')
    plt.title('Icy Days As a Function of Year')
    plt.savefig("data_plot.jpg")

def q3(csvfile):
    data = pd.read_csv(csvfile)
    data["year"] = data["year"].astype(int)
    data["year"] = (data["year"] - min(data["year"])) / (max(data["year"]) - min(data["year"]))
    n = len(data)
    aarr = np.ones((n,2))
    aarr[:, 0] = data["year"]
    return aarr

def q4(sX, filename):
    data = pd.read_csv(filename)
    data["days"] = data["days"].astype(int)
    Y = data["days"].to_numpy()
    wb = np.matmul(np.linalg.inv(np.matmul(sX.transpose(), sX)) , np.matmul(sX.transpose(), Y))
    return wb

def grad_desc(alpha, rang, filename):
    data = q3(filename)
    ys = pd.read_csv(filename)["days"].astype(int)
    n = len(data)
    wb = np.zeros(2)
    loss_data = []
    for iteration in range(rang):

        if iteration % 10 == 0:
            print(wb)

        # find the loss before the iteration runs through
        loss_sum = 0
        for i in range(n):
            loss_sum += (wb[0] * data[i, 0] + wb[1] - ys[i])**2
        loss = 1 / (2*n) * loss_sum
        loss_data.append(loss)
        
        # re-assign the weight and bias
        
        yihat = np.matmul(wb.transpose(), data.transpose())
        grad = 1/n * np.matmul(np.subtract(yihat, ys), data)
        wb = wb - alpha * grad

    iterations_data = [i for i in range(rang)] # these will be the x values
    plt.plot(iterations_data, loss_data)
    plt.xlabel('Iteration Number')
    plt.ylabel('Loss')
    plt.savefig("loss_plot.jpg")
    return wb

def q6(filename):
    wb = q4(q3(filename), filename)
    data = pd.read_csv(filename)
    data["year"] = data["year"].astype(int)
    computation = (2023 - min(data["year"])) / (max(data["year"]) - min(data["year"]))
    answer = wb[0] * computation + wb[1]
    return answer

def q7(w):
    w = int(w)
    if w < 0:
        return "<"
    elif w > 0:
        return ">"
    elif w == 0:
        return "="

def q8(filename):
    wb = q4(q3(filename), filename)
    data = pd.read_csv(filename)
    data["year"] = data["year"].astype(int)
    x_star = (-wb[1] * (max(data["year"]) - min(data["year"])) / wb[0]) + min(data["year"])
    return x_star

if __name__ == "__main__":
    # set up the system arguments
    filename = sys.argv[1]
    learning_rate = float(sys.argv[2])
    iterations = int(sys.argv[3])

    # data has already been cleaned and saved, so no need to call clean_data
    
    # call the visualization function (q2)
    vis(filename)
    
    # implement q3 (normalize the data)
    print("Q3:")
    print(q3(filename))
    
    # implement q4 (get the closed solution w and b)
    print("Q4:")
    print(q4(q3(filename), filename))

    # run gradient descent (q5)
    print("Q5a:")
    grad_desc(learning_rate, iterations, filename)
    print("Q5b: 0.38")
    print("Q5c: 400")

    # predict the data point (q6)
    print("Q6: " + str(q6(filename)))

    # interpret the weight (q7)
    print("Q7a: " + q7(q4(q3(filename), filename)[0]))
    print("Q7b: A weight greater than zero indicates that the when the year increases by one unit, the number of ice days increases by an amount w. A weight less than zero indicates that when the year increases by 1 unit, the number of ce days decreases by an amount absolute value of w. A weight of zero indicates that the amount of ice days is not affected by this feature")

    # find the year it will no longer freeze (q8)
    print("Q8a: " + str(q8(filename)))
    print("Q8b: Based on the available data, it is thought that in the year predicted above, the lake will no longer have any days where it is frozen over. This could be a plausible prediction due to the high rates of global warming and emissions directly affecting the ecosystem. While more features may lead to a more informed prediction (as there could be other contributing factors), this is still a realistic base model.")
    