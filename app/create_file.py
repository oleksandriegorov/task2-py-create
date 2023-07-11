# write your code here
import argparse
import datetime
import os
import sys


class CreateFileCustomException(Exception):
    pass


def create_directory(rpath: str) -> None:
    os.makedirs(rpath, exist_ok=True)
    return rpath


def get_header():
    current_date_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{current_date_stamp}\n"


def write_data_file(contents_from_cli, file_path):
    with open(file_path, "a") as fh:
        stamp = get_header()
        fh.write(stamp)
        fh.writelines(
            (f"{idx+1} {line}\n" for idx, line in enumerate(contents_from_cli))
        )
        fh.write("\n")


def get_contents_from_cli():
    contents_from_cli = []
    while (content_line := input("Enter content line: ")) != "stop":
        contents_from_cli.append(content_line)
    return contents_from_cli


def main():
    arg_parser = argparse.ArgumentParser()
    req_args_grp = arg_parser.add_argument_group(
        title="Main arguments",
        description="At least one of below arguments are required",
    )
    req_args_grp.add_argument(
        "-f", "--file", help="Name of a file to write input strings to"
    )
    req_args_grp.add_argument(
        "-d",
        "--directory",
        nargs="*",
        help="Name of a file to write input strings to",
    )
    prog_args = arg_parser.parse_args()
    data_file = prog_args.file
    data_dir = prog_args.directory
    current_dir = os.getcwd()
    try:
        if not data_file:
            if not data_dir:
                arg_parser.print_usage()
                sys.exit(0)
            else:
                new_dir = create_directory(
                    os.path.join(
                        current_dir,
                        *data_dir,
                    )
                )
                print(f"Directory {new_dir} was created")
                print("Provide a file name using -f to start contents input")
                sys.exit(0)
        elif not data_dir:
            write_to_dir = current_dir
        else:  # implies data_dir
            write_to_dir = os.path.join(current_dir, *data_dir)
            create_directory(write_to_dir)
        contents_from_cli = get_contents_from_cli()
        file_path = os.path.join(write_to_dir, data_file)
        write_data_file(contents_from_cli, file_path)

    except Exception as e:
        raise CreateFileCustomException(
            "Could not create a file and fill it in with data properly"
        ) from e


if __name__ == "__main__":
    main()
