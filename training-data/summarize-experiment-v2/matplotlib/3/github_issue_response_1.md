GitHub Bug Title:
Markers are not hollow when using ax.scatter() and setting markers.MarkerStyle()'s fillstyle to 'none'.

Description:
When setting markers to be hollow by using ax.scatter() and setting markers.MarkerStyle's fillstyle parameter to 'none', the desired effect is not achieved. Instead, the markers appear filled. 

Reproduction Steps:
1. Import required modules
2. Create random data for scatter plot
3. Use ax.scatter() and markers.MarkerStyle to set markers hollow
4. Display the plot using plt.show()

Expected Output:
The markers should appear hollow when setting markers.MarkerStyle's fillstyle parameter to 'none'.

Environment:
- Python: 3.7.3.final.0
- matplotlib: 3.1.2
- numpy: 1.18.1