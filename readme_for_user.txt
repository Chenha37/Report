Dear user,
In order to run the algorithm, you should enter the "best_three_players_algorithm" notebook on Jupyter.
The last window in the notebook has a line to fill the input to the algorithm:

x = external_best_three_players_algorithm(rf_model, dataset.iloc[shuffled_indices[:num_train]], 1000000, producers_list, directors_list, writers_list)
print(x)

The algorithm decletarion is:
def external_best_three_players_algorithm(rf_model, df_train, budget, producers_list, directors_list, writers_list):

you as a user should fill the producers list, the directors list, the writers list,
and the budget, and then run everything :)

Hope you will found our algorithm useful, and have the most successful film!! :)
Chen&Tal 
 