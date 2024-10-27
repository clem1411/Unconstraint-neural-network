import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_csv(file_path):
    # Read the full CSV file
    data = pd.read_csv(file_path)
    if data.shape[1] < 2:
        raise ValueError("CSV file must contain at least two columns")
    
    # Generate an index column for full data plot
    data.insert(0, 'Index', range(len(data)))
    return data

def plot_last50_csv(file_path):
    # Read and slice to include only the last 50 generations
    data = pd.read_csv(file_path)
    if data.shape[1] < 2:
        raise ValueError("CSV file must contain at least two columns")
    
    # Generate an index column for last 50 data plot
    data = data.tail(50)
    data.insert(0, 'Index', range(len(data)))
    return data

def update_plots(frame, file_path, line1, line2, line3, line4):
    # Update full data plot
    full_data = plot_csv(file_path)
    line1.set_data(full_data['Index'], full_data.iloc[:, 1])
    line2.set_data(full_data['Index'], full_data.iloc[:, 2])

    # Update last 50 data plot
    last50_data = plot_last50_csv(file_path)
    line3.set_data(last50_data['Index'], last50_data.iloc[:, 1])
    line4.set_data(last50_data['Index'], last50_data.iloc[:, 2])

    # Rescale both plots
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    return line1, line2, line3, line4

# Set up the figure and subplots
file_path = 'fitness_data.csv'
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Initial plot for the overall data (left subplot)
full_data = plot_csv(file_path)
line1, = ax1.plot(full_data['Index'], full_data.iloc[:, 1], label='Maximum')
line2, = ax1.plot(full_data['Index'], full_data.iloc[:, 2], label='Average')
ax1.set_xlabel('Generation')
ax1.set_ylabel('Fitness score')
ax1.set_title('Full CSV Data Plot')
ax1.legend()

# Initial plot for the last 50 generations (right subplot)
last50_data = plot_last50_csv(file_path)
line3, = ax2.plot(last50_data['Index'], last50_data.iloc[:, 1], label='Maximum')
line4, = ax2.plot(last50_data['Index'], last50_data.iloc[:, 2], label='Average')
ax2.set_xlabel('Generation')
ax2.set_ylabel('Fitness score')
ax2.set_title('Last 50 Generations Plot')
ax2.legend()

# Animation to update both plots every minute
ani = animation.FuncAnimation(fig, update_plots, fargs=(file_path, line1, line2, line3, line4), interval=60000)

plt.tight_layout()
plt.show()
