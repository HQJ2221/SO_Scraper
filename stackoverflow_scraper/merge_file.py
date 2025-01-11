import json
import os
import re


def merge_txt_files(source_folder, output_folder, files_per_merge=1000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_count = 0
    merge_count = 0
    outfile = None

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.txt'):
                if file_count % files_per_merge == 0:
                    if outfile:
                        outfile.write("]\n")
                        print(f"File {output_file} created.")
                        outfile.close()
                    merge_count += 1
                    output_file = os.path.join(output_folder, f'merged_{merge_count}.json')
                    outfile = open(output_file, 'w', encoding='utf-8')
                    outfile.write("[\n")
                else:
                    if outfile:
                        outfile.write(",\n")


                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    problem, solution = formatting(infile)
                    data = {"problem": problem, "solution": solution}
                    json.dump(data, outfile, ensure_ascii=False, indent=4)

                file_count += 1

    if outfile:
        outfile.write("]\n")
        print(f"File {output_file} created.")
        outfile.close()


def formatting(file):
    mode = 0
    space_num = 0
    pbs = ""
    slt = ""
    while True:
        line = file.readline()
        if not line:
            break

        line = line.strip()
        line = re.sub(r"'problems'", "\"problems\"", line)
        line = re.sub(r"'solutions'", "\"solutions\"", line)

        for match in re.finditer(r"('(.*)')|(\"(.*)\")", line):
            raw = match.group(0).strip()
            if raw[0] == "'" and raw[-1] == "'":
                raw = raw[1:-1]
            elif raw[0] == '"' and raw[-1] == '"':
                raw = raw[1:-1]

            if raw == "\\n":
                space_num += 1
                continue
            else:
                if space_num > 1:
                    raw = "\n" + raw
                space_num = 0

            if raw[-2:] == "\\n":
                raw = raw[:-2] + "\n"

            if raw == "solutions" or raw == "problems":
                if raw == "solutions":
                    mode = 1
                continue

            raw = raw.replace("\\'", "'")

            if mode == 1 and raw == "............................................................":
                return pbs, slt

            if mode == 0:
                pbs += raw
            else:
                slt += raw

    return pbs, slt


if __name__ == "__main__":
    source_folder = '../qa'
    output_folder = 'merged_files'
    merge_txt_files(source_folder, output_folder)
