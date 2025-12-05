import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


df = pd.read_csv('IMDB Top 250 Movies.csv')

real_gen = ""
for i in df['genre']:
    real_gen = real_gen+","+i
all_gen = real_gen.split(',')[1:]
unique_genres = list(set(all_gen))

data = []
for i in unique_genres:
    c = 0
    for j in df['genre']:
        if i in j:
            c+=1
    data.append([i, c])
    
gen_df = pd.DataFrame(data, columns=['Genre', 'Freq'])
gen_df.sort_values(by = 'Freq', ascending = False, inplace = True)
gen_df = gen_df.head(5)

plt.figure(figsize=(12,6),dpi = 150)
sns.barplot(data = gen_df, x = 'Genre', y = 'Freq', palette='Paired')
plt.title('Top 5 most Popular Genre')
plt.show()

fig = px.box(df, x='genre', y='box_office', color='genre', title='Box Office by Genre')
fig.show()