import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import spearmanr
from SALib.sample import saltelli


problem = {
    'num_vars': 3,
    'names': ['cost of fight', 'avg food per oasis', 'total food in domain'],
    'bounds': [
        [10, 100],
        [50, 200],
        [80, 300],
    ]
}


param_values = saltelli.sample(problem, 128)
results = np.load("Type_experiment/results.npy")

# Output structure:
# [Total Pop, Anxious, Resentful, Random, Flexible, Show-off]
output_names = ['Total', 'Anxious', 'Resentful', 'Random', 'Flexible', 'Show-off']

df = pd.DataFrame(results, columns=output_names)
params_df = pd.DataFrame(param_values, columns=['cost of fight', 'avg food per oasis', 'total food'])

# Merge for easier plotting
full_df = pd.concat([params_df, df], axis=1)

# --- 1. Correlation heatmap of types ---
corr = df[output_names[1:]].corr(method='spearman')  # exclude Total
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='vlag', center=0)
plt.title("Spearman Correlation between Crew Types")
plt.tight_layout()
plt.savefig("correlation_types.png", dpi=300)
plt.close()

# --- 2. Scatter: Anxious vs each other type ---
for t in output_names[2:]:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=df[t], y=df['Anxious'])
    plt.xlabel(f'{t} Population')
    plt.ylabel('Anxious Population')
    plt.title(f'Anxious vs {t}')
    plt.tight_layout()
    plt.savefig(f"Type_experiment/anxious_vs_{t.lower()}.png", dpi=300)
    plt.close()


# Simple regression-style diagnostic
import statsmodels.api as sm

X = full_df[['cost of fight', 'Resentful', 'Show-off', 'Random', 'Flexible']]
X = sm.add_constant(X)
y = full_df['Anxious']

model = sm.OLS(y, X).fit()
print(model.summary())
