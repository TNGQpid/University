from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # Your implementation goes here!
    images = np.load("face_dataset.npy") # this is an n x m matrix, where n is the number of images and m is the number of features (pixels)
    images = images - np.mean(images, axis = 0)
    return images
    # raise NotImplementedError

def get_covariance(dataset):
    # Your implementation goes here!
    XT = np.transpose(dataset)
    cov_mat = 1/(np.shape(dataset)[0]-1) * np.dot(XT, dataset) # this makes it an m x m matrix (4096 x 4096)
    #print(np.size(cov_mat)) # it should be m x m
    return cov_mat
    # raise NotImplementedError

def get_eig(S, m):
    n = np.shape(S)[0] # get the number of eigenvalues, which is also the number of rows
    eivalues, eivectors = eigh(S, subset_by_index = [n - m, n - 1])
    # print(eivalues, eivectors)
    # to reverse them, do a reverse python slice
    eivalues, eivectors = eivalues[::-1], eivectors[:, ::-1]
    # make the eivalues a diagnoal matrix like the question wants
    eivalues = np.diag(eivalues)
    return eivalues, eivectors
    #raise NotImplementedError

def get_eig_prop(S, prop):
    vally = []
    lambdas = eigh(S, eigvals_only = True)
    listy = lambdas.tolist()
    total = sum(listy)
    for item in listy:
        if item / total > prop:
            vally.append(item)
    vally.sort()
    #print(vally)
    start, end = vally[0], vally[-1]
    eivalues, eivectors = eigh(S, subset_by_value = [start - 0.0001, np.inf]) # the 0.0001 is because the parameter is exclusive, inclusive and we want
    # it to be inclusive, inclusive
    eivalues, eivectors = eivalues[::-1], eivectors[:, ::-1]
    eivalues = np.diag(eivalues)
    return eivalues, eivectors
    #print(eivalues)
    #raise NotImplementedError

def project_image(image, U):
    # Your implementation goes here!
    # print(np.shape(image))
    listy = [] # this will be a list of all the weights (alphas)
    for i in range(np.shape(U)[1]):
        listy.append(np.dot(image, U[:, i]))
    listy
    XiPCA = np.zeros(np.shape(image)[0])
    for i in range(np.shape(U)[1]):
        XiPCA += listy[i] * U[:, i]
    return XiPCA
    #raise NotImplementedError

def display_image(orig, proj):
    # Your implementation goes here!
    # Please use the format below to ensure grading consistency
    # fig, ax1, ax2 = plt.subplots(figsize=(9,3), ncols=2)
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    ax1.set_title("Original")
    ax2.set_title("Projection")
    im1 = ax1.imshow(orig.reshape(64,64), aspect = "equal")
    im2 = ax2.imshow(proj.reshape(64,64), aspect = "equal")
    fig.colorbar(im1, ax = ax1, location = "right")
    fig.colorbar(im2, ax = ax2, location = "right")
    return fig, ax1, ax2
    #raise NotImplementedError

def perturb_image(image, U, sigma):
    # Your implementation goes here!
    listyy = [] # this will be a list of all the weights (alphas)
    for i in range(np.shape(U)[1]):
        listyy.append(np.dot(image, U[:, i])+ np.random.normal(scale=sigma))
    XiPCA = np.zeros(np.shape(image))
    for i in range(np.shape(U)[1]):
        XiPCA += listyy[i] * U[:, i]
    return XiPCA
    #raise NotImplementedError

def combine_image(image1, image2, U, lam):
    # Your implementation goes here!
    alpha1 = [] # this will be a list of all the weights (alphas)
    for i in range(np.shape(U)[1]):
        alpha1.append(np.dot(image, U[:, i]))
    alpha2 = []
    for i in range(np.shape(U)[1]):
        alpha2.append(np.dot(image2, U[:, i]))
    # combine the two lists in the way specified
    alpha_comb = [lam*a + (1 - lam)*b for a,b in zip(alpha1, alpha2)]
    combination = np.zeros(np.shape(image))
    for i in range(np.shape(U)[1]):
        combination += alpha_comb[i] * U[:, i]
    return combination
    #raise NotImplementedError