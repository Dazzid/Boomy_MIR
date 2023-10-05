#%%
import numpy as np
import matplotlib.pyplot as plt

#%%
# load X from a numpy file
X = np.load('/Users/lcros/Downloads/X.npy')
X_rolling = np.load('/Users/lcros/Downloads/X_rolling.npy')

# print some statistics about the data
print(X.shape)
print(np.mean(X, axis=0))
print(np.std(X, axis=0))

# chroma_mean is the first 12 features
# chroma_std is the next 12 features
# tempo is the last feature
chroma_mean = X[:, :12]
chroma_std = X[:, 12:24]
tempo = X[:, 24]

tempo_rolling = X_rolling[:, 24]

#%%
# plot the histogram of the tempo, comparing the two datasets
plt.hist(tempo, bins=20, alpha=0.5, label='Boomy')
plt.hist(tempo_rolling, bins=20, alpha=0.5, label='Rolling Stone')
plt.legend(loc='upper right')
plt.show()

# plot a boxplot of the tempo using seaborn
import seaborn as sns
sns.boxplot(tempo)
plt.show()

# %%
import pandas as pd
# plot the boxplot of the chroma mean in a more readable way using seaborn
df = pd.DataFrame(chroma_mean)
df.columns = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
plt.figure(figsize=(10, 6))
sns.boxplot(data=df)
# y axis
plt.ylabel('Chroma mean accross time')
plt.show()

# %%
# plot the chroma means using a violin plot stacked
plt.figure(figsize=(10, 6))
sns.violinplot(data=df, inner=None, color='lightgray')
sns.stripplot(data=df, size=4, jitter=True)
# y axis
plt.ylabel('Chroma mean accross time')
plt.show()

# %%
df.head()
# %%
# plot the chroma means with ridge plot in seaborn in multiple rows

g = sns.FacetGrid(df, row="variable", hue="variable", aspect=15, height=.5, palette='colorblind')

# Draw the densities in a few steps
g.map(sns.kdeplot, "value",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "value", clip_on=False, color="w", lw=2, bw_adjust=.5)

# passing color=None to refline() uses the hue mapping
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, 'value')

# Set the subplots to not overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap and space them out
g.set_titles("")
g.set(yticks=[])
g.set(ylabel="")
g.set(xlabel="")
g.despine(bottom=True, left=True)

# %%
# save the dataframe
df.to_csv('/Users/lcros/Downloads/chroma_mean_rolling.csv', index=False)