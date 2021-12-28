<p align="center"><a href="https://twitter.com/Aprender_alemao"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/twitter.png" alt="Twitter" title="Twitter" width="50"/></a><a href="https://www.facebook.com/estudaralemao/"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/facebook.png" alt="Facebook" title="Facebook" width="50"/></a><a href="https://www.instagram.com/estudaralemao/"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/instagram.png" alt="Instagram" title="Instagram" width="50"/></a><a href="https://www.youtube.com/c/wwwqueroestudaralemaocombr"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/youtube.png" alt="YouTube" title="YouTube" width="50"/></a><a href="https://api.whatsapp.com/send?phone=5511989782756&text=I%20want%20to%20know%20..."><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/whatsapp.png" alt="WhatsApp" title="WhatsApp" width="50"/></a><a href="https://www.queroestudaralemao.com.br"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/website.png" alt="WWW" title="WWW" width="50"/></a><a href="https://br.pinterest.com/chucrutehans/"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/pinterest.png" alt="Pinterest" title="Pinterest" width="50"/></a><a href="mailto:aulasparticularesdealemaosp@gmail.com?subject=I%20want%20to%20know%20...%20"><img src="https://cdn.jsdelivr.net/gh/dmhendricks/signature-social-icons/icons/round-flat-filled/50px/mail.png" alt="E-Mail" title="E-Mail" width="50"/>
</a>


<p align="center">
<a href=https://github.com/hansalemaos><img src="https://img.shields.io/badge/author-hansalemaos-black"/></a>
<a href=https://www.queroestudaralemao.com.br><img src="https://img.shields.io/badge/from-queroestudaralemao.com.br-darkgreen"/></a>
<a href=#><img src="https://img.shields.io/badge/for-Windows-black"/></a>
<a href=https://codeload.github.com/liangjingkanji/DrakeTyporaTheme/zip/refs/heads/master><img src="https://img.shields.io/badge/Theme-Drake-black"/></a>
<a href=https://github.com/dmhendricks/signature-social-icons><img src="https://img.shields.io/badge/Social-Icons-darkgreen"/></a>
</p><br><!--  -->

# DirDF

Are you one of those people who have never any space on their hard disk? Do you spend hours and hours searching for your files because you never remember where you saved them? Well, since I am one of those, I tried several tools in the past: [TreeSize](https://www.jam-software.com/treesize_free) / [WinDirStat](https://windirstat.net/) / [WizTree](https://diskanalyzer.com/) / [SpaceSniffer](http://www.uderzo.it/main_products/space_sniffer/) / GREP. They all are great,

but take forever to get the job done and only offer limited filter functions. Around 5 hours ago, after having searched around 30 minutes for a file on my hard drive, I decided to do something about it. Since [pandas](https://github.com/pandas-dev/pandas) is the greatest invention of mankind (eighth wonder of the world?), I thought: why not using the power of pandas to solve this problem once and for all?

Now, about 5 hours later, the first version of “DirDF” is ready, and I am really happy with the results (I found the file I was looking for in a couple of seconds hahaha)

## how to use it
### Creating an instance
```
search_folder = DirDF(

    path_to_search=r"F:\\zzzzzzzzzzzzzzzzzzzzzzzzzz1", save_df_to=r"F:\\saveto"

)
```
**path_to_search** = you can pass a string or a list (more than one path)  
**save_df_to** = the search results will be saved in this folder so that you can use them later on

### Preparing flat copy
```
search_folder.create_flatcopy_link(separator="Ç", saveto=r"F:\\symlinks")
```

This function will create a column in the DataFrame with the filenames for “flat copy” (all files in one folder).  It will not copy anything yet!  
**separator="Ç"** means that the backslash ‘\\’ will be replaced by “Ç”. The replacement is important because there is not “flat copy” with a backslash in the path!

### Performing a flat copy (symlink)
```
search_folder.create_simlink_in_folder(filtered_df=search_folder.df, printresult=True)
```

Here we perform the “flat copy” that we prepared in the last command. Important: the files are not copied, only a symlink is created (to save space hahaha).

<img src="symlink.png" width="800"/>
<img src="symlink1.png" width="800"/>


### Performing a flat copy (real copy)
```
search_folder.create_flatcopy_link(seperator="#", saveto=r"F:\\symlinks")
search_folder.flatcopyfiles(filtered_df=search_folder.df, printresult=True)
```
Here we perform the “flat copy” but this time, the files are copied!

<img src="flatcopy.png" width="800"/>


### Regex search in file content
```
all_txt_files = search_folder.df.loc[search_folder.df.f_filepath.str.contains("\\.txt$")].copy() #**The filter functions of pandas are awesome! Let’s filter all txt files.**

**

searchresultsdf = search_folder.search_with_regex_in_files(

    regular_expression=r"[^\\n]+Bilderraten\[^\\n]+",

    df=all_txt_files,

    ignorecase=False,

    dotall=False,

    printresult=True,

    use_bs4=True

)

```

Here I perform a regex search in all TXT files. **If you don’t pass a filtered DataFrame, search_folder.df will be used. The results are returned as a DataFrame**

<img src="regexsearch.png" width="800"/>

### DataFrame beaaaautifuuuuul 
```
search_folder.printdf(start=1, how_many_lines=1000)
```
A print function to make the DataFrame look more beautiful.

<img src="print.png" width="800"/>

### Delete files
```
search_folder.delete_files(filtered_df=all_txt_files, printresult=True, ask_before=True)
```
This function will delete all files in the filtered DataFrame. **If you don’t pass a filtered DataFrame, search_folder.df will be used.** ***It will always ask before deleting a file, unless you pass “ask_before=False”***
<img src="deletefiles.png" width="800"/>