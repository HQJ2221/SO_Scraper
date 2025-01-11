import json
import os


def filter_null_solution(src_folder, dst_folder, min_merge_per_file=1600):
    total_len = 0
    test_len = 0
    merge_num = 1
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
    outfile = open(f"{dst_folder}/fil_{merge_num}.json", "w", encoding="utf-8")
    tot_data = []

    for root, _, files in os.walk(src_folder):
        for file in files:
            if test_len > min_merge_per_file:
                print(f"File fil_{merge_num}.json has {test_len} items.")
                merge_num += 1
                test_len = 0
                json.dump(tot_data, outfile, ensure_ascii=False, indent=4)
                outfile.close()
                outfile = open(f"{dst_folder}/fil_{merge_num}.json", "w", encoding="utf-8")
                tot_data = []

            with open(os.path.join(root, file), "r") as f:
                data = json.loads(f.read())
            filtered_data = [item for item in data if item.get("solution")]
            # print(f"{file}: {len(filtered_data)} data after filter.")
            test_len += len(filtered_data)
            total_len += len(data)
            tot_data.extend(filtered_data)

    print(f"File fil_{merge_num}.json has {test_len} items.")
    json.dump(tot_data, outfile, ensure_ascii=False, indent=4)
    outfile.close()
    print(f"Total data: {total_len}")


if __name__=="__main__":
    filter_null_solution("merged_files", "filtered_files")

