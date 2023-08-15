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

data = []
labels = []

for class_subdir in class_subdirectories:
    class_data = []

    class_directory = os.path.join(data_directory, class_subdir)

    for prefix in target_prefixes:
        class_labels = []  # Initialize class_labels here for each prefix

        for filename in os.listdir(class_directory):
            if filename.startswith(prefix) and filename.endswith(".txt"):
                file_path = os.path.join(class_directory, filename)

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                for line in lines:
                    parts = line.split('\t')
                    timestamp = float(parts[0])
                    direction_length = float(parts[1])

                    class_data.append([timestamp, direction_length])
                    class_labels.append(class_subdir)  # Append to class_labels only once per file

        labels.extend(class_labels)  # Move this line outside of the prefix loop

    data.extend(class_data)

data_array = np.array(data)

# Perform PCA with 2 components
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_array)  # Define data_pca after performing PCA

# Visualize the results
plt.figure(figsize=(10, 8))

# Convert class labels to colors using the defined dictionary
label_colors = [colors[label] for label in labels]

plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label_colors, alpha=0.5)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Visualization of Data")
plt.colorbar(label="Class")

plt.savefig("/scratch/VF/Visualization_data/result.jpg")
