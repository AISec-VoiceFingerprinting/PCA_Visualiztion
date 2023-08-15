import os
import shutil

source_directory = '/scratch/VF/unzip_data/available_class_parsing'
destination_directory = '/scratch/VF/Visualization_data/class_3'

# 원하는 파일 이름의 시작 부분들
target_prefixes = [
    "493", "495", "496", "500", "507", "508", "509"
]

# 복사하는 파일 개수 제한
files_to_copy_per_prefix = 10
total_files_to_copy = len(target_prefixes) * files_to_copy_per_prefix
files_copied_count = 0

# 각 시작 숫자별로 파일 복사
copied_counts_by_prefix = {prefix: 0 for prefix in target_prefixes}
not_copied_files_by_prefix = {prefix: [] for prefix in target_prefixes}

for prefix in target_prefixes:
    copied_files_for_prefix = 0

    for filename in os.listdir(source_directory):
        if filename.startswith(prefix) and filename.endswith(".txt"):
            source_path = os.path.join(source_directory, filename)
            destination_path = os.path.join(destination_directory, filename)

            try:
                shutil.copy(source_path, destination_path)
                print(f"파일 {filename} 이(가) 복사되었습니다.")
                files_copied_count += 1
                copied_files_for_prefix += 1
                copied_counts_by_prefix[prefix] += 1

                if copied_files_for_prefix >= files_to_copy_per_prefix:
                    break

            except FileNotFoundError:
                not_copied_files_by_prefix[prefix].append(filename)

        if files_copied_count >= total_files_to_copy:
            break

    if files_copied_count >= total_files_to_copy:
        break

print(f"num of total copied files : {files_copied_count} ")

# 각 시작 이름별로 복사된 파일 개수 프린트
for prefix, count in copied_counts_by_prefix.items():
    print(f"copied {prefix} : {count} files")

# 각 시작 이름별로 복사되지 않은 파일 이름 프린트
for prefix, filenames in not_copied_files_by_prefix.items():
    if filenames:
        print(f"{prefix} , not available:")
        for filename in filenames:
            print(filename)
