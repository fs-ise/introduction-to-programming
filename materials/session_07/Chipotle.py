import pandas as pd

chipo = pd.read_csv('Chipotle.csv')

#1 Display the first 10 entries
chipo.head(10)

#2 What is the number of observations in the dataset?
chipo.shape[0]

#3 What is the number of columns in the dataset?
chipo.shape[1]

#4 Print the names of all the columns as a list.
list(chipo)

#5 How many items were ordered in total?
chipo['quantity'].sum()

#6 How many different items are sold?
chipo['item_name'].value_counts().count()

#7 How many orders were made in the period?
chipo['order_id'].value_counts().count()

#8 How much was the revenue for the period in the dataset? Solve without creating a new column 'revenue'.
(chipo['quantity']* chipo['item_price']).sum()

#9 What is the average revenue amount per order? Solve with creating a new column 'revenue'.
chipo['revenue'] = chipo['quantity'] * chipo['item_price']
chipo.groupby('order_id')['revenue'].sum().mean()

#10 Which was the most-ordered item?
chipo.groupby('item_name').sum().sort_values(['quantity'], ascending=False).head(1)

#11 How many products cost more than $10.00?
chipo.loc[chipo.item_price>10, 'item_price'].count()

#12 What was the quantity of the most expensive item ordered?
chipo.loc[chipo.item_price==chipo.item_price.max(), 'quantity']

#13 How many times was a Veggie Salad Bowl ordered?
chipo[chipo.item_name == "Veggie Salad Bowl"].shape[0]
len(chipo[chipo.item_name == "Veggie Salad Bowl"])

#14 How many times did someone order more than one Canned Soda?
chipo[(chipo.item_name == "Canned Soda") & (chipo.quantity > 1)].shape[0]
len(chipo[(chipo.item_name == "Canned Soda") & (chipo.quantity > 1)])

#15 Create a bar chart of the top 5 items bought
chipo['item_name'].value_counts().head(5).plot(kind='bar', xlabel='Items', ylabel='Number of Times Ordered', title='Most ordered Chipotles Items', rot=20)

#16 Create a scatterplot with the number of items orderered per order price
chipo.groupby('order_id').sum().plot(kind='scatter', x='quantity', y='item_price', xlabel='Items ordered', ylabel='Order Price', title='Number of items ordered per order price')






