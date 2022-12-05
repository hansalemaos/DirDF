# -*- coding: utf-8 -*-
import subprocess
from functools import reduce

import regex
from flexible_partial import FlexiblePartialOwnName
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)
import os
import pandas as pd
from LatinFixer import wrong_chars

from fastfilecopy import copyfile, movefile
from touchtouch import touch

forbiddenfilepath = [":", "?", "*", "<", '"', ">", "|"]

latindict = {
    "¡": "\\302\\241",
    "¢": "\\302\\242",
    "£": "\\302\\243",
    "¤": "\\302\\244",
    "¥": "\\302\\245",
    "¦": "\\302\\246",
    "§": "\\302\\247",
    "¨": "\\302\\250",
    "©": "\\302\\251",
    "ª": "\\302\\252",
    "«": "\\302\\253",
    "¬": "\\302\\254",
    "®": "\\302\\256",
    "¯": "\\302\\257",
    "°": "\\302\\260",
    "±": "\\302\\261",
    "²": "\\302\\262",
    "³": "\\302\\263",
    "´": "\\302\\264",
    "µ": "\\302\\265",
    "¶": "\\302\\266",
    "·": "\\302\\267",
    "¸": "\\302\\270",
    "¹": "\\302\\271",
    "º": "\\302\\272",
    "»": "\\302\\273",
    "¼": "\\302\\274",
    "½": "\\302\\275",
    "¾": "\\302\\276",
    "¿": "\\302\\277",
    "À": "\\303\\200",
    "Á": "\\303\\201",
    "Â": "\\303\\202",
    "Ã": "\\303\\203",
    "Ä": "\\303\\204",
    "Å": "\\303\\205",
    "Æ": "\\303\\206",
    "Ç": "\\303\\207",
    "È": "\\303\\210",
    "É": "\\303\\211",
    "Ê": "\\303\\212",
    "Ë": "\\303\\213",
    "Ì": "\\303\\214",
    "Í": "\\303\\215",
    "Î": "\\303\\216",
    "Ï": "\\303\\217",
    "Ð": "\\303\\220",
    "Ñ": "\\303\\221",
    "Ò": "\\303\\222",
    "Ó": "\\303\\223",
    "Ô": "\\303\\224",
    "Õ": "\\303\\225",
    "Ö": "\\303\\226",
    "×": "\\303\\227",
    "Ø": "\\303\\230",
    "Ù": "\\303\\231",
    "Ú": "\\303\\232",
    "Û": "\\303\\233",
    "Ü": "\\303\\234",
    "Ý": "\\303\\235",
    "Þ": "\\303\\236",
    "ß": "\\303\\237",
    "à": "\\303\\240",
    "á": "\\303\\241",
    "â": "\\303\\242",
    "ã": "\\303\\243",
    "ä": "\\303\\244",
    "å": "\\303\\245",
    "æ": "\\303\\246",
    "ç": "\\303\\247",
    "è": "\\303\\250",
    "é": "\\303\\251",
    "ê": "\\303\\252",
    "ë": "\\303\\253",
    "ì": "\\303\\254",
    "í": "\\303\\255",
    "î": "\\303\\256",
    "ï": "\\303\\257",
    "ð": "\\303\\260",
    "ñ": "\\303\\261",
    "ò": "\\303\\262",
    "ó": "\\303\\263",
    "ô": "\\303\\264",
    "õ": "\\303\\265",
    "ö": "\\303\\266",
    "÷": "\\303\\267",
    "ø": "\\303\\270",
    "ù": "\\303\\271",
    "ú": "\\303\\272",
    "û": "\\303\\273",
    "ü": "\\303\\274",
    "ý": "\\303\\275",
    "þ": "\\303\\276",
    "ÿ": "\\303\\277",
}
latintuple2 = (
    ("Â¡", "¡"),
    ("Â¢", "¢"),
    ("Â£", "£"),
    ("Â¤", "¤"),
    ("Â¥", "¥"),
    ("Â¦", "¦"),
    ("Â§", "§"),
    ("Â¨", "¨"),
    ("Â©", "©"),
    ("Âª", "ª"),
    ("Â«", "«"),
    ("Â¬", "¬"),
    ("Â®", "®"),
    ("Â¯", "¯"),
    ("Â°", "°"),
    ("Â±", "±"),
    ("Â²", "²"),
    ("Â³", "³"),
    ("Â´", "´"),
    ("Âµ", "µ"),
    ("Â¶", "¶"),
    ("Â·", "·"),
    ("Â¸", "¸"),
    ("Â¹", "¹"),
    ("Âº", "º"),
    ("Â»", "»"),
    ("Â¼", "¼"),
    ("Â½", "½"),
    ("Â¾", "¾"),
    ("Â¿", "¿"),
    ("Ã", "À"),
    ("Ã", "Á"),
    ("Ã", "Â"),
    ("Ã", "Ã"),
    ("Ã", "Ä"),
    ("Ã", "Å"),
    ("Ã", "Æ"),
    ("Ã", "Ç"),
    ("Ã", "È"),
    ("Ã", "É"),
    ("Ã", "Ê"),
    ("Ã", "Ë"),
    ("Ã", "Ì"),
    ("Ã", "Í"),
    ("Ã", "Î"),
    ("Ã", "Ï"),
    ("Ã", "Ð"),
    ("Ã", "Ñ"),
    ("Ã", "Ò"),
    ("Ã", "Ó"),
    ("Ã", "Ô"),
    ("Ã", "Õ"),
    ("Ã", "Ö"),
    ("Ã", "×"),
    ("Ã", "Ø"),
    ("Ã", "Ù"),
    ("Ã", "Ú"),
    ("Ã", "Û"),
    ("Ã", "Ü"),
    ("Ã", "Ý"),
    ("Ã", "Þ"),
    ("Ã", "ß"),
    ("Ã ", "à"),
    ("Ã¡", "á"),
    ("Ã¢", "â"),
    ("Ã£", "ã"),
    ("Ã¤", "ä"),
    ("Ã¥", "å"),
    ("Ã¦", "æ"),
    ("Ã§", "ç"),
    ("Ã¨", "è"),
    ("Ã©", "é"),
    ("Ãª", "ê"),
    ("Ã«", "ë"),
    ("Ã¬", "ì"),
    ("Ã­", "í"),
    ("Ã®", "î"),
    ("Ã¯", "ï"),
    ("Ã°", "ð"),
    ("Ã±", "ñ"),
    ("Ã²", "ò"),
    ("Ã³", "ó"),
    ("Ã´", "ô"),
    ("Ãµ", "õ"),
    ("Ã¶", "ö"),
    ("Ã·", "÷"),
    ("Ã¸", "ø"),
    ("Ã¹", "ù"),
    ("Ãº", "ú"),
    ("Ã»", "û"),
    ("Ã¼", "ü"),
    ("Ã½", "ý"),
    ("Ã¾", "þ"),
    ("Ã¿", "ÿ"),
    ("Ã\\237", "ß"),
    ("Ã\\207", "Ç"),
    ("Ã", "Ç"),
)
latindictopp = {v: k for k, v in latindict.items()}
latindictoppyuple = tuple(latindictopp.items())
wrong_chars_sorted = tuple(reversed(sorted(wrong_chars, key=lambda x: x[0])))


def _create_symlink(src: str, dest: str) -> bool:
    if not os.path.exists(dest):
        touch(dest)
        os.remove(dest)
    try:
        os.symlink(src, dest, False)
    except Exception:
        return False
    return True


def get_dataframe_from_folder(
    folder, ls_path="ls", last_access_time=True, exit_keys="ctrl+x", timeout=None,
):
    command = f'"{ls_path}" -1 -R -i -H --hyperlink -las -s -f --full-time --context'
    if last_access_time:
        command = (
            f'"{ls_path}" -1 -R -i -H --hyperlink -las -s -f --full-time --context -c'
        )

    folder = os.path.normpath(folder)
    workdict = os.getcwd()
    os.chdir(folder)
    print_output = False
    mydata = execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=command,
        subcommands=[],
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )
    os.chdir(workdict)
    df = pd.DataFrame(mydata)
    df[0] = df[0].apply(lambda x: x.decode("latin", "ignore"))
    df = df.loc[~df[0].str.contains(r"[.]{1,2}\s*$", regex=True, na=False)]
    df[0] = df[0].apply(
        lambda x: reduce(
            lambda a, b: a.replace(b[0], b[1]), latindictoppyuple, x
        ).strip()
    )
    df[0] = df[0].apply(
        lambda x: reduce(lambda a, b: a.replace(b[0], b[1]), latintuple2, x).strip()
    )
    df[0] = df[0].str.lstrip()
    df["aa_folder"] = df[0].str.extract(r"^([\'.:]{0,5}/.*)")
    df["aa_folder"] = df.aa_folder.str.rstrip("/:").str.lstrip("./")
    df.aa_folder = df.aa_folder.ffill()

    df = df.fillna("")
    df = df.loc[df[0].str.contains(r"^\d+\s+")]
    dfcomplete = df[0].str.split(n=10, expand=True).copy()
    symlink = dfcomplete[10].str.split(" -> ", regex=False, expand=True)
    if symlink.shape[1] == 1:
        symlink[1] = pd.NA
    df = pd.concat(
        [dfcomplete, df.aa_folder.copy(), symlink], axis=1, ignore_index=True
    )
    df["aa_date"] = pd.to_datetime(df[7] + " " + df[8] + " " + df[9])
    df = df.drop(columns=[7, 8, 9])
    df.columns = [
        "aa_id",
        "aa_rights",
        "aa_links",
        "aa_owner",
        "aa_group",
        "aa_security",
        "aa_size",
        "aa_complete_data",
        "aa_relative_folder",
        "aa_filename",
        "aa_symlink",
        "aa_date",
    ]

    df["aa_folder"] = df.aa_relative_folder.apply(
        lambda x: os.path.normpath(os.path.join(folder, x))
    )
    df.aa_relative_folder = df.aa_relative_folder.apply(lambda x: os.path.normpath(x))
    df.aa_symlink = df.aa_symlink.apply(
        lambda x: os.path.normpath(regex.sub(r"^/(\w)/", r"\g<1>:\\", x.strip()))
        if isinstance(x, str)
        else pd.NA
    )
    df.aa_relative_folder = df.aa_relative_folder.str.replace(r"^\.$", "", regex=True)
    df["aa_fullpath"] = df.aa_folder + "\\" + df.aa_filename
    df = df.drop(columns="aa_complete_data").reset_index(drop=True)
    df = df.filter(list(sorted(df.columns)))
    df.aa_relative_folder = df.aa_relative_folder.str.replace("/", "\\")

    try:
        df["aa_filename"] = df["aa_filename"].astype("string")
    except Exception:
        pass
    try:
        df["aa_folder"] = df["aa_folder"].astype("category")
    except Exception:
        pass
    try:
        df["aa_fullpath"] = df["aa_fullpath"].astype("string")
    except Exception:
        pass
    try:
        df["aa_symlink"] = df["aa_symlink"].astype("string")
    except Exception:
        pass
    try:
        df["aa_size"] = df["aa_size"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_index"] = df["aa_index"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_rights"] = df["aa_rights"].astype("category")
    except Exception:
        pass
    try:
        df["aa_links"] = df["aa_links"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_owner"] = df["aa_owner"].astype("category")
    except Exception:
        pass
    try:
        df["aa_group"] = df["aa_group"].astype("category")
    except Exception:
        pass
    try:
        df["aa_security"] = df["aa_security"].astype("category")
    except Exception:
        pass
    try:
        df["aa_relative_folder"] = df["aa_relative_folder"].astype("category")
    except Exception:
        pass
    try:
        df["aa_id"] = df["aa_id"].astype("Int64")
    except Exception:
        pass

    dftype = df.loc[(df.aa_size > 0) & (~df.aa_rights.str.startswith("l"))].index
    df["aa_filetype"] = pd.NA
    df.loc[dftype, "aa_filetype"] = df.loc[dftype].aa_filename.str.extract(
        r"(\.[^\./\\]+$)"
    )[0]
    try:
        df["aa_filetype"] = df["aa_filetype"].astype("category")
    except Exception:
        pass
    return df


def flatcopy_sorted(
    src, file_ending, dest_folder, foldersep="ǀ", symlink=False, copystat=True
):
    if not isinstance(file_ending, str):
        file_ending = "other"
    dest_folder = os.path.join(dest_folder, file_ending.strip("."))
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest = replace_non_valid_chars_file_path(src, replacement="_")
    desta = os.path.join(dest_folder, dest.replace(os.sep, foldersep))
    if symlink:
        _create_symlink(src=src, dest=desta)
    else:
        if not copystat:
            copyfile(src, desta, copystat=False)
        else:
            copyfile(src, desta, copystat=True)

    return desta


def replace_non_valid_chars_file_path(string_, replacement="_"):
    return reduce(lambda a, b: a.replace(b, replacement), forbiddenfilepath, string_)


def flatcopy(src, dest_folder, foldersep="ǀ", symlink=False, copystat=True):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest = replace_non_valid_chars_file_path(src, replacement="_")
    desta = os.path.join(dest_folder, dest.replace(os.sep, foldersep))
    if symlink:
        _create_symlink(src=src, dest=desta)
    else:
        if not copystat:
            copyfile(src, desta, copystat=False)
        else:
            copyfile(src, desta, copystat=True)

    return desta


def move_file(src, dest_folder, copystat=True):
    fpa = regex.sub(r"^[^:]+:\\", "", src)
    print(fpa)
    dest_folder_file = os.path.join(dest_folder, fpa)
    print(dest_folder_file)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    if not os.path.exists(dest_folder_file):
        touch(dest_folder_file)
        os.remove(dest_folder_file)
    print(src, dest_folder_file)
    return movefile(src, dest_folder_file, copystat=copystat)


def rip_grep_search(
    rip_grep_path,
    path,
    regular_expression,
    other_parameters="",
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):

    return b"".join(
        execute_subprocess_multiple_commands_with_timeout_bin(
            rf'{rip_grep_path} {other_parameters} --search-zip --line-number --case-sensitive --binary "{regular_expression}" "{path}"',
            subcommands=[],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
    )


def get_string(
    strings_path, filepath, exit_keys: str = "ctrl+x", print_output=True, timeout=None,
):
    xx = b"".join(
        execute_subprocess_multiple_commands_with_timeout_bin(
            rf'{strings_path} "{filepath}"',
            subcommands=[],
            exit_keys=exit_keys,
            print_output=print_output,
            timeout=timeout,
        )
    )
    return xx.split(b"www.sysinternals.com\r\n\r\n")[-1]


def get_fzf(
    fzf_path, strings_path, filepath, searchstring,
):
    stringp = get_string(strings_path, filepath=filepath, print_output=False).strip()

    processNames = subprocess.run(
        [
            fzf_path,
            "-f",
            searchstring,
            "--sync",
            "--layout=reverse",
            "--no-multi",
            "--inline-info",
            "--no-sort",
        ],
        input=stringp,
        capture_output=True,
    )
    return processNames.stdout


def add_functions(
    df,
    strings_path="strings",
    fzf_path="fzf",
    rip_grep_path="rg.exe",
    add_flatcopy_sorted=True,
    add_flatcopy=True,
    add_extract_strings=True,
    add_fuzzy_extract=True,
    add_ripgrep=True,
    add_open_file=True,
    add_move_file=True,
):
    if add_flatcopy_sorted:
        df["ff_flatcopy_sorted"] = df.apply(
            lambda x: FlexiblePartialOwnName(
                flatcopy_sorted,
                f"dest_folder:str, foldersep:str='ǀ', symlink:bool=False, copystat:bool=True",
                True,
                x.aa_fullpath,
                x.aa_filetype,
            ),
            axis=1,
        )
    if add_extract_strings:
        df["ff_extract_strings"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(
                get_string,
                f"exit_keys:str='ctrl+x', print_output:bool=True, timeout:Union[None,int]=None",
                True,
                strings_path,
                x,
            )
        )
    if add_extract_strings or add_fuzzy_extract:
        df["ff_fuzzy"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(
                get_fzf, f"searchstring:str", True, fzf_path, strings_path, x,
            )
        )
    if add_ripgrep:
        df["ff_ripgrep"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(
                rip_grep_search,
                f"regular_expression:str, other_parameters:str='', exit_keys:str='ctrl+x', print_output:bool=True, timeout:Union[None,int]=None",
                True,
                rip_grep_path,
                x,
            )
        )

    if add_open_file:
        df["ff_open"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(os.startfile, f"", True, x,)
        )
    if add_move_file:
        df["ff_move_file"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(
                move_file, f"dest_folder:str, copystat:bool=True", True, x,
            )
        )
    if add_flatcopy:
        df["ff_flatcopy"] = df.aa_fullpath.apply(
            lambda x: FlexiblePartialOwnName(
                flatcopy,
                f"dest_folder:str, foldersep:str='ǀ', symlink:bool=False, copystat:bool=True",
                True,
                x,
            )
        )
    return df


def get_df_from_folder_with_functions(
    folder,
    ls_path="ls",
    last_access_time=True,
    exit_keys="ctrl+x",
    timeout=None,
    strings_path="strings",
    fzf_path="fzf",
    rip_grep_path="rg.exe",
    add_flatcopy_sorted=True,
    add_flatcopy=True,
    add_extract_strings=True,
    add_fuzzy_extract=True,
    add_ripgrep=True,
    add_open_file=True,
    add_move_file=True,
):

    df = get_dataframe_from_folder(
        folder,
        ls_path=ls_path,
        last_access_time=last_access_time,
        exit_keys=exit_keys,
        timeout=timeout,
    )
    df = add_functions(
        df,
        strings_path=strings_path,
        fzf_path=fzf_path,
        rip_grep_path=rip_grep_path,
        add_flatcopy_sorted=add_flatcopy_sorted,
        add_flatcopy=add_flatcopy,
        add_extract_strings=add_extract_strings,
        add_fuzzy_extract=add_fuzzy_extract,
        add_ripgrep=add_ripgrep,
        add_open_file=add_open_file,
        add_move_file=add_move_file,
    )
    return df


def pd_add_dfdir():
    pd.Q_folder_to_df = get_dataframe_from_folder
    pd.Q_folder_to_df_with_functions = get_df_from_folder_with_functions
