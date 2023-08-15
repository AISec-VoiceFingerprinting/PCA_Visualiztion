import os
import numpy as np
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Read data from TXT files
data_directory = "/scratch/VF/Visualization_data"
class_subdirectories = ["class_1", "class_2", "class_3"]
target_prefixes = ["309", "357", "383", "384", "385", "386", "389", "390", "391", "414", "416", "417",
                   "063", "225", "226", "428", "284", "285", "287", "288", "289", "432", "292",
                   "493", "495", "496", "500", "507", "508", "509"]

colors = {'class_1': 'red', 'class_2': 'blue', 'class_3': 'yellow'}

# Initialize data and labels lists
data = []
labels = []

# Loop through class subdirectories
for class_subdir in class_subdirectories:

    class_directory = os.path.join(data_directory, class_subdir)

    # Loop through target prefixes
    for prefix in target_prefixes:

        # Find the most suitable data points for the current file
        selected_data_points = []

        for filename in os.listdir(class_directory):
            if filename.startswith(prefix) and filename.endswith(".txt"):
                file_path = os.path.join(class_directory, filename)

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                # Initialize variables for best, middle, and last data points
                best_timestamp = float('inf')
                middle_timestamp = 0
                last_timestamp = 0

                best_direction_length = None
                middle_direction_length = None
                last_direction_length = None

                # Process each line in the file
                for line in lines:
                    parts = line.split('\t')
                    timestamp = float(parts[0])
                    direction_length = float(parts[1])

                    # Update data points based on timestamps
                    if timestamp < best_timestamp:
                        best_timestamp = timestamp
                        best_direction_length = direction_length

                    if timestamp > last_timestamp:
                        last_timestamp = timestamp
                        last_direction_length = direction_length

                # Calculate middle data point only if both best and last data points are available
                if best_direction_length is not None and last_direction_length is not None:
                    middle_timestamp = (best_timestamp + last_timestamp) / 2
                    middle_direction_length = (best_direction_length + last_direction_length) / 2

                    # Append suitable data points to the list
                    selected_data_points.append([best_timestamp, best_direction_length])
                    selected_data_points.append([middle_timestamp, middle_direction_length])
                    selected_data_points.append([last_timestamp, last_direction_length])

        # Append the selected data points to the overall data and labels lists
        for data_point in selected_data_points:
            data.append(data_point)
            labels.append(class_subdir)

# Convert data and labels to arrays
data_array = np.array(data)
labels_array = np.array(labels)

# Perform PCA with 2 components
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_array)

# Visualize the results
plt.figure(figsize=(10, 8))

# Convert class labels to colors using the defined dictionary
label_colors = [colors[label] for label in labels_array]

plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label_colors, alpha=0.5)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Visualization of Data")

plt.savefig("/scratch/VF/Visualization_data/result_OnedotEach.jpg")
