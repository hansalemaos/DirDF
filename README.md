### Never mind explorer.exe, here is dirdf

Are you one of those people who have never any space on their hard disk? Do you spend hours and hours searching for your files because you never remember where you saved them? Well, since I am one of those, I tried several tools in the past: TreeSize / WinDirStat / WizTree / SpaceSniffer / GREP. They all are great,

but take forever to get the job done and only offer limited filter functions. Around 5 hours ago, after having searched around 30 minutes for a file on my hard drive, I decided to do something about it ... 

#### Install the package (Windows only)
```python
pip install dirdf
```

#### Install Cygwin (ls.exe is necessary for getting the file list)

[ls.exe](https://www.cygwin.com/setup-x86_64.exe).

#### Tools needed for some functions

[strings.exe](https://download.sysinternals.com/files/Strings.zip).
[rg.exe](https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep-13.0.0-x86_64-pc-windows-gnu.zip).
[fzf.exe](https://github.com/junegunn/fzf/releases/download/0.35.1/fzf-0.35.1-windows_amd64.zip).

##### It is recommended to add strings.exe/rg.exe/fzf.exe/ls.exe files to your path

```python
from dirdf import pd_add_dfdir
pd_add_dfdir()
import pandas as pd

df = pd.Q_folder_to_df(
    folder=r"C:\Users\blabla",
    ls_path="ls",
    last_access_time=True,
    exit_keys="ctrl+x",
    timeout=None,
)
df2 = pd.Q_folder_to_df_with_functions(
    folder=r"C:\Users\blabla",
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
)

# Some examples

# Flatcopy - foldersep='ǀ' means that the backslash ‘\’ will be replaced by 'ǀ'. The replacement is important because there is no “flat copy” with a backslash in the path! All file types (pdf, jpg ... ) will get their own folder. If you want to save space, create a symlink instead of copying the whole file 
df.loc[df.aa_fullpath.str.contains(r'\.txt|\.docx|\.jpg')][:100].ff_flatcopy_sorted.apply(lambda x:x('f:\\testflatcopy_df', foldersep='ǀ', symlink=False, copystat=True))
df.loc[df.aa_fullpath.str.contains(r'\.txt|\.docx|\.jpg')][:100].ff_flatcopy_sorted.apply(lambda x:x('f:\\testflatcopy_df\\symlink', foldersep='ǀ', symlink=True, copystat=True)) # copystat will be ignored in this case

# Flatcopy without sorting file types
df.loc[df.aa_fullpath.str.contains(r'\.txt')][2:100].ff_flatcopy.apply(lambda x:x('f:\\newfoldertest\\flatcopy'))
df.loc[df.aa_fullpath.str.contains(r'\.txt')][2:100].ff_flatcopy.apply(lambda x:x('f:\\newfoldertest\\flatcopy\\sym',symlink=True))

# Extract all strings from any file 
df.loc[df.aa_fullpath.str.contains(r'\.txt')][:100].ff_extract_strings.apply(lambda x:x(exit_keys='ctrl+x', print_output=True, timeout=None))

# Fuzzy search in any file
df.loc[df.aa_fullpath.str.contains(r'\.txt')][:100].ff_fuzzy.apply(lambda x:x('windows'))

# Regex search in any file
df.loc[df.aa_fullpath.str.contains(r'\.txt')][:100].ff_ripgrep.apply(lambda x:x(regular_expression='name', other_parameters='-i', exit_keys='ctrl+x', print_output=True, timeout=.1))

# Executes os.startfile()
df.loc[df.aa_fullpath.str.contains(r'\.txt')][:100].iloc[0].ff_open()

# Moves files, keeps the folder structur
df.loc[df.aa_fullpath.str.contains(r'\.txt')][:1].ff_move_file.apply(lambda x:x('f:\\newfoldertest'))


df
Out[3]: 
                               aa_date  ... aa_filetype
0  2022-10-23 12:18:58.767317900-03:00  ...          .0
1  2022-10-23 05:48:51.755017400-03:00  ...       .yaml
2  2022-10-23 05:51:47.520702700-03:00  ...        .jpg
3  2022-10-23 05:51:46.817189600-03:00  ...        .jpg
4  2022-10-23 05:48:51.755017400-03:00  ...       .yaml
5  2022-10-23 12:18:58.767317900-03:00  ...        .csv
6  2022-10-23 05:51:49.630625800-03:00  ...        .jpg
7  2022-10-23 05:51:52.116036400-03:00  ...        .jpg
8  2022-10-23 05:51:52.678404900-03:00  ...        .jpg
9  2022-10-23 13:31:03.003835900-03:00  ...         NaN
10 2022-10-23 12:18:59.267762600-03:00  ...         .pt
11 2022-10-23 06:00:01.068658100-03:00  ...         .pt
12 2022-10-23 07:23:56.117463800-03:00  ...         .pt
13 2022-10-23 08:53:33.799414100-03:00  ...         .pt
14 2022-10-23 12:18:59.048534200-03:00  ...         .pt
[15 rows x 14 columns]
df2
Out[4]: 
                               aa_date  ...                                        ff_flatcopy
0  2022-10-23 12:18:58.767317900-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
1  2022-10-23 05:48:51.755017400-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
2  2022-10-23 05:51:47.520702700-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
3  2022-10-23 05:51:46.817189600-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
4  2022-10-23 05:48:51.755017400-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
5  2022-10-23 12:18:58.767317900-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
6  2022-10-23 05:51:49.630625800-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
7  2022-10-23 05:51:52.116036400-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
8  2022-10-23 05:51:52.678404900-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
9  2022-10-23 13:31:03.003835900-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
10 2022-10-23 12:18:59.267762600-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
11 2022-10-23 06:00:01.068658100-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
12 2022-10-23 07:23:56.117463800-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
13 2022-10-23 08:53:33.799414100-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
14 2022-10-23 12:18:59.048534200-03:00  ...  dest_folder:str, foldersep:str='ǀ', symlink:bo...
[15 rows x 21 columns]


```

