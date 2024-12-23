


# plt.figure()
# sns.lineplot(x='TimeToFeeding', y='Active', data=proportion)
# plt.show()
#
#
# plt.figure()
# sns.lineplot(x='TimeToFeeding', y='Active', hue='FeederIntervalC', data=proportion)
# plt.show()
# #
# # #%%
# #
# #
# #
# # selected_data = data.query('TimeToFeeding > 100 and TimeToFeeding < 200')
# # transition_matrix1 = Transition.compute_transition_matrix(selected_data)
# # print(transition_matrix1)
# #
# # selected_data = data.query('TimeToFeeding < 30')
# # transition_matrix2 = Transition.compute_transition_matrix(selected_data)
# # print(transition_matrix2)
# #
# # plt.figure()
# # plt.subplot(1, 2, 1)
# # sns.heatmap(transition_matrix1, annot=True, cmap='grey', cbar=False, vmin=0, vmax=1)
# # plt.xlabel('Current State')
# # plt.ylabel('Previous State')
# # plt.subplot(1, 2, 2)
# # sns.heatmap(transition_matrix2, annot=True, cmap='grey', cbar=False, vmin=0, vmax=1)
# # plt.xlabel('Current State')
# # plt.ylabel('Previous State')
# # plt.show()
# #
# # cats = list(data.Subject.unique())
