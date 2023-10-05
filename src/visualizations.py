# %%
import umap
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
from sklearn.preprocessing import MinMaxScaler
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.stats import gaussian_kde
import seaborn as sns
from matplotlib.patches import Rectangle
# Set the random seed for reproducibility
np.random.seed(0)
# %%
# load the file "/Users/lcros/Downloads/penultimate_array.npy" 
boomy = np.load("/Users/lcros/Downloads/penultimate_array.npy")
print(boomy.shape)
# load titles from /Users/lcros/Downloads/titles.npy
titles = np.load("/Users/lcros/Downloads/titles.npy", allow_pickle=True)

#%%
# remove the middle dimension
boomy = boomy.reshape(boomy.shape[0], boomy.shape[-1])
# %%
# VISUALIZE THE TUNES USING TSNE and UMAP

# load real from the file "/Users/lcros/Downloads/penultimate_array_rollingStones.npy"
real = np.load("/Users/lcros/Downloads/penultimate_array_rollingStones.npy")
# remove the middle dimension
real = real.reshape(real.shape[0], real.shape[-1])
# boomy = []

# %%
print(real.shape)
print(boomy.shape)
# %%
# create a TSNE object and fit the data of both real and boomy
all_tsne = TSNE(n_components=2, perplexity=20, n_iter=1000, init='pca',
                random_state=10, learning_rate='auto').fit_transform(np.concatenate((real, boomy), axis=0))
real_tsne = all_tsne[0:len(real)]
gen_tsne = all_tsne[len(real):]

# Umap is also a good alternative
all_umap = umap.UMAP(n_components=2, n_neighbors=5,
                        min_dist=0.3, metric='correlation', random_state=10).fit_transform(np.concatenate((real, boomy), axis=0))
real_umap = all_umap[0:len(real)]
gen_umap = all_umap[len(real):]

#%%
print(real_tsne.shape)
print(gen_tsne.shape)

# %%
# get the index of the tune that contains 'onkey' in the title
idx = np.where([True if 'onkey' in title else False for title in titles])[0][0]

#%%
# visualize the tunes in a 2D scatter plot
print('TSNE')
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(real_tsne[:, 0], real_tsne[:, 1], c='r', label='Rolling stones 500')
ax.scatter(gen_tsne[:, 0], gen_tsne[:, 1], c='b', label='Boomy')
idxs1 = np.where((gen_umap[:, 0] < 2.5))[0]
# get where gen_umap[:, 1] > 6 & gen_umap[:,0] < -0.4 as idx2
idxs2 = np.where((gen_umap[:, 1] > 6) & (gen_umap[:, 0] < -0.4))[0]
# plot the tunes in idxs1 in a different color
ax.scatter(gen_tsne[idxs1, 0], gen_tsne[idxs1, 1], c='g', label='Boomy - outliers 1')
# # plot the tunes in idxs2 in a different color
# ax.scatter(gen_tsne[idxs2, 0], gen_tsne[idxs2, 1], c='y', label='Boomy - outliers 2')
# # plot the tune that contains 'onkey' in the title in a different color
# ax.scatter(gen_tsne[idx, 0], gen_tsne[idx, 1], c='r', label='Monkey')
ax.grid()
ax.legend()
# %%
# visualize the tunes in a 2D scatter plot with Umap
print('UMAP')
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(real_umap[:, 0], real_umap[:, 1], c='r', label='Rolling stones 500')
ax.scatter(gen_umap[:, 0], gen_umap[:, 1], c='b', label='Boomy')
ax.scatter(gen_umap[idxs1, 0], gen_umap[idxs1, 1], c='g', label='Boomy - outliers 1')
# ax.scatter(gen_umap[idxs2, 0], gen_umap[idxs2, 1], c='y', label='Boomy - outliers 2')
# ax.scatter(gen_umap[idx, 0], gen_umap[idx, 1], c='r', label='Monkey')
ax.grid()
ax.legend()

#%%
# # print the names of the tunes that are in the left side of the scatter plot
print('outliers 1:')
for i in idxs1:
    print(titles[i])

# # print the names of the tunes that are in the right side of the scatter plot
# print('\noutliers 2:')
# for i in idxs2:
#     print(titles[i])
