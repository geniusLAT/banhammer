import re


def check_profanity(user_line: str) -> bool:
    profanity_lines = separate_file_content_to_lines()
    for line in profanity_lines:
        # for letter in line:
        #     print(f"{ord(letter)} : {letter}")
        # print(f"checking line: |{line}| in text:|{user_line}|")
        # print(f"checking line: |{len(line)}| in text:|{len(user_line)}|")
        if re.search(line.strip(), user_line, re.IGNORECASE):
            return True
    return False


def separate_file_content_to_lines(
    file_path: str = "filter_profanity_russian_cached.txt",
) -> list:
    file_content = open_file_for_filtering(file_path)
    if file_content is not None:
        return file_content.splitlines()
    else:
        return []


def open_file_for_filtering(file_path: str = "filter_profanity_russian_cached.txt"):
    try:
        with open(f"src/resources/{file_path}", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found in resources folder.")
        return None


if __name__ == "__main__":
    print(check_profanity("input()"))
