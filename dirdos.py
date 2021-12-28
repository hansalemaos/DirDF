import os
import shutil
from collections import defaultdict
from copy import deepcopy
from time import strftime, sleep
import regex  # pip install regex
import pandas as pd  # pip install pandas
from bs4 import BeautifulSoup  # pip install bs4
from random import randrange
import gc
import kthread  # pip install kthread
from farbprinter.farbprinter import Farbprinter  # pip install farbprinter
import numpy as np

forbiddenfilepath = ["\\", "/", ":", "?", "*", "<", '"', ">", "|"]

drucker = Farbprinter()


class DirDF:
    def __init__(self, path_to_search, save_df_to):
        if isinstance(path_to_search, str):
            path_to_search = [path_to_search]
        path_to_search = [x.rstrip("\\") for x in path_to_search]
        path_to_search = [x + "\\" for x in path_to_search]
        self.ergebnisdict = self.nesteddicterstellen()
        self.save_df_to = save_df_to
        self.path_to_search = path_to_search
        allethreads = [
            kthread.KThread(
                target=self.getfilelist_mit_dir_ms_dos, args=[xxx], name=xxx[0]
            )
            for xxx in path_to_search
        ]
        allethreads2 = [k.start() for k in allethreads]
        while len(path_to_search) > len(list(self.ergebnisdict.keys())):
            sleep(0.5)
        gc.collect()
        alledatenframeszusammen = []
        for key, item in self.ergebnisdict.items():
            datenframeneu = pd.read_pickle(item)
            alledatenframeszusammen.append(datenframeneu)
        df = pd.concat(alledatenframeszusammen)
        df.reset_index(inplace=True, drop=True)
        gc.collect()
        df.index = df.index.astype("int32")
        df.f_folder = df.f_folder.astype("category")
        df.f_filename = df.f_filename.astype("string")
        df.f_filepath = df.f_filepath.astype("string")
        df.f_owner = df.f_owner.astype("category")
        df["f_date"] = df.f_date + " " + df.f_time
        df["f_date"] = df["f_date"].astype("datetime64")
        df.drop(columns=["f_time"], inplace=True)
        df.f_size = df.f_size.str.replace(r"\.", "", regex=True)
        df = df.loc[df.f_size.str.contains("^\d+$")].copy()
        df.f_size = df.f_size.astype("int64")
        self.endergebnisfilename = (
            save_df_to + "\\" + strftime("%Y_%m_%d_%H_%M_%S") + ".pkl"
        )
        df.reset_index(inplace=True, drop=True)
        df.to_pickle(self.endergebnisfilename)
        self.df = df.copy()
        gc.collect()

    def printdf(self, start=1, how_many_lines=1000):
        drucker.p_pandas_list_dict(
            self.df[start : start + how_many_lines], linebreak=1000
        )

    def flatcopyfiles(self, filtered_df=None, printresult=True):
        if filtered_df is None:
            filtered_df = self.df

        def _copy_file(src, dest):
            try:
                if os.path.isfile(src):
                    dpath, dfile = os.path.split(dest)
                    if not os.path.isdir(dpath):
                        os.makedirs(dpath)
                    try:
                        shutil.copy2(src, dest)
                        return True
                    except Exception as Fehler:
                        print(Fehler)
                        return False
            except:
                return False
            return False

        for link, symlink in zip(
            filtered_df.f_filepath.to_list(), filtered_df.flatcopy.to_list()
        ):
            funktioniert = _copy_file(src=link, dest=symlink)
            if printresult is True:
                if funktioniert is True:
                    print(drucker.f.black.brightgreen.italic(f"{link} -> {symlink} OK"))
                elif funktioniert is False:
                    print(
                        drucker.f.black.brightred.italic(f"{link} -> {symlink} ERROR")
                    )

    def flattenlist_neu(self, iterable):
        def iter_flatten(iterable):
            it = iter(iterable)
            for e in it:
                if isinstance(e, (list)):
                    for f in iter_flatten(e):
                        yield f
                else:
                    yield e

        a = [i for i in iter_flatten(iterable)]
        return a

    def readfile(self, pfad, minlength=4, deleteemptylines=True, use_bs4=True):
        try:
            with open(pfad, mode="rb") as f:
                dateiohnehtml = f.read()
            if use_bs4 is False:
                return dateiohnehtml
            dateiohnehtml = (
                b"""<!DOCTYPE html><html><body><p>"""
                + dateiohnehtml
                + b"""</p></body></html>"""
            )
            soup = BeautifulSoup(dateiohnehtml, "lxml")
            soup = soup.text
            soup = soup.strip()
            if deleteemptylines is True:
                versteckt = [x for x in soup.splitlines() if len(x) > minlength]
                return versteckt
            if deleteemptylines is False:
                return soup
        except Exception as Fehler:
            print(Fehler)

    def nesteddicterstellen(self):
        nested_dict = lambda: defaultdict(nested_dict)
        nest = nested_dict()
        return deepcopy(nest)

    def getfilelist_mit_dir_ms_dos(self, pfad):
        aktuellezeit = strftime("%Y_%m_%d_%H_%M_%S")
        aktuellezeit = aktuellezeit + str(randrange(0, 1000000000000000000)).zfill(25)
        os.system(
            rf"dir {pfad} /A/OD/R/S/TC/c/4 > {self.save_df_to}\verstecktedateiensuchemitdirmsdos{aktuellezeit}.txt"
        )
        alledateien = self.readfile(
            rf"{self.save_df_to}\verstecktedateiensuchemitdirmsdos{aktuellezeit}.txt"
        )
        speicherpfad = rf"{self.save_df_to}\ergebnis{aktuellezeit}.pkl"
        aktuellesfolder = ""
        msdosfileliste = self.nesteddicterstellen()
        msdosfileliste[aktuellesfolder] = []
        for a in alledateien:
            a = a.strip()
            leerzeichen = regex.findall("^\s*$", a)
            if any(leerzeichen):
                continue
            folderda = regex.findall("^Directory.*", a)
            folderda = self.flattenlist_neu(folderda)
            if any(folderda):
                aktuellesfolder = folderda[0]
                if not folderda[0] in msdosfileliste.keys():
                    msdosfileliste[folderda[0]] = []
            fileda = regex.findall("^\d\d\.\d\d.\d\d\d\d.*", a)
            fileda = self.flattenlist_neu(fileda)
            if any(fileda):
                try:
                    msdosfileliste[aktuellesfolder].append(fileda[0])
                except:
                    msdosfileliste[aktuellesfolder] = []
                    msdosfileliste[aktuellesfolder].append(fileda[0])
        alleergebnismsdossuche = []
        for key in msdosfileliste.keys():
            infos = msdosfileliste[key]
            for liste in infos:
                dateiengefunden = regex.findall(
                    r"(^[\d\.]+)\s+([\d:]+)(.{19})(.*)", str(liste)
                )
                dateiengefunden = self.flattenlist_neu(dateiengefunden)
                if any(dateiengefunden):
                    try:
                        zwischenergebnis = [
                            key,
                            dateiengefunden[0][0],
                            dateiengefunden[0][1],
                            dateiengefunden[0][2],
                            dateiengefunden[0][3],
                        ]
                        alleergebnismsdossuche.append(zwischenergebnis.copy())
                    except Exception as Fehler:
                        print(Fehler)
        mdf = pd.DataFrame.from_records(
            alleergebnismsdossuche,
            columns=["folder", "aenderungsdatum", "uhrzeit", "groesse", "dateiname"],
        )
        mdf.folder = mdf.folder.str.replace(r"^\s*Directory\s*of\s*", "", regex=True)
        mdf.groesse = mdf.groesse.str.strip()
        mdf["datei"] = mdf[mdf.groesse.str.isnumeric()].groesse.apply(
            lambda x: int(regex.sub("\.", "", x))
        )
        mdf["dateiname"] = mdf.dateiname.str.strip()

        mdf["besitzer"] = mdf.dateiname.str.extract(r"^\s*(.[^\\]+)[\\].*")
        mdf["besitzer"] = mdf.besitzer.str.strip("\\")
        mdf.dateiname = mdf.dateiname.str.replace(r"^\s*(.[^\\]+)[\\]", "", regex=True)
        mdf.dateiname = mdf.dateiname.str.replace("Administra", "", regex=False)
        mdf.columns = [
            "f_folder",
            "f_date",
            "f_time",
            "f_size",
            "f_filename",
            "f_file",
            "f_owner",
        ]
        mdf["f_filepath"] = mdf.f_folder + "\\" + mdf.f_filename
        mdf.drop_duplicates(subset=["f_filepath"], inplace=True)
        mdf = mdf.loc[
            ~mdf.f_filename.str.contains("^\.*$", regex=True, na=False)
        ].copy()
        mdf.reset_index(inplace=True, drop=True)
        mdf.to_pickle(speicherpfad)
        self.ergebnisdict[aktuellezeit] = speicherpfad
        # return mdf.copy(),aktuellezeit

    def sortsize(self):
        self.df.sort_values(by=["f_size"], inplace=True, ascending=False)

    def p(self, liste):
        for indi, li in enumerate(liste):
            if indi % 2 == 0:
                print(drucker.f.black.brightwhite.normal(f"{indi}\t{li}"))
                continue
            print(drucker.f.brightwhite.black.normal(f"{indi}\t{li}"))
            continue

    forbiddenfilepath = ["\\", "/", ":", "?", "*", "<", '"', ">", "|"]

    def create_flatcopy_link(self, separator, saveto):
        def _create_flatcopy_link(seperator, folder, saveto):
            if seperator in forbiddenfilepath:
                seperator = ";"
            folder = folder.replace("\\", seperator)
            folder = folder[3:]
            saveto = saveto.strip("\\ ")
            return saveto + "\\" + folder

        self.df["flatcopy"] = self.df.f_filepath.apply(
            lambda x: _create_flatcopy_link(
                seperator=separator, folder=x, saveto=saveto
            )
        )

    def create_simlink_in_folder(self, filtered_df=None, printresult=True):
        if filtered_df is None:
            filtered_df = self.df

        def create_symlink(dateipfad, symlink):
            'use like this: create_symlink(r"c:\folder oder file with\shi--y name", "nicename", withending=False)'
            try:
                if os.path.islink(symlink) is True:
                    os.remove(symlink)
            except:
                pass
            try:
                os.symlink(dateipfad, symlink)
            except:
                return False
            return True

        for link, symlink in zip(
            filtered_df.f_filepath.to_list(), filtered_df.flatcopy.to_list()
        ):
            funktioniert = create_symlink(dateipfad=link, symlink=symlink)
            if printresult is True:
                if funktioniert is True:
                    print(drucker.f.black.brightgreen.italic(f"{link} -> {symlink} OK"))
                elif funktioniert is False:
                    print(
                        drucker.f.black.brightred.italic(f"{link} -> {symlink} ERROR")
                    )

    def delete_files(self, filtered_df=None, printresult=True, ask_before=True):
        if filtered_df is None:
            filtered_df = self.df
        for file in filtered_df.f_filepath.to_list():
            deleting = True
            if ask_before is True:
                inputuser = input(
                    drucker.f.black.brightwhite.bold(
                        f" Do you want to delete: {file} ??? 1 = YES / ANY OTHER KEY = NO"
                    )
                )
                if inputuser != "1":
                    deleting = False
            if deleting is True:
                try:
                    os.remove(file)
                    if printresult:
                        print(drucker.f.black.brightgreen.italic(f"{file} REMOVED"))
                    continue

                except:
                    if printresult:
                        print(drucker.f.black.brightred.italic(f"{file} ERROR"))
            print(drucker.f.black.brightred.italic(f"{file} NOT REMOVED"))

    def search_with_regex_in_files(
        self,
        regular_expression,
        df=None,
        ignorecase=False,
        dotall=False,
        printresult=True,
        use_bs4=True,
    ):
        regexsearch = regex.compile(regular_expression)
        try:
            if df.empty is False:
                filtered_df = df.copy()
        except:
            pass
        try:
            if df is None:
                filtered_df = self.df.copy()
        except:
            pass

        if ignorecase is True and dotall is True:
            regexsearch = regex.compile(
                regular_expression, regex.DOTALL | regex.IGNORECASE
            )
        if ignorecase is True and dotall is False:
            regexsearch = regex.compile(regular_expression, regex.IGNORECASE)
        if ignorecase is False and dotall is True:
            regexsearch = regex.compile(regular_expression, regex.DOTALL)

        def _search_with_regex_in_files(file):
            fileconent = self.readfile(
                file, minlength=1, deleteemptylines=False, use_bs4=use_bs4
            )
            print(fileconent)
            ergebnis = regexsearch.findall(str(fileconent))
            if any(ergebnis):
                if printresult:
                    for ergi in ergebnis:
                        print(
                            drucker.f.black.brightyellow.underline(
                                f"     Results in {file}:      "
                            )
                        )
                        print(drucker.f.black.brightgreen.italic(ergi))
                return ergebnis
            return np.nan

        filtered_df["content"] = np.nan
        filtered_df["content"] = filtered_df["content"].astype("object")
        filtered_df["content"] = filtered_df.f_filepath.apply(
            _search_with_regex_in_files
        )
        return filtered_df.copy()


# search_folder = DirDF(
#     path_to_search=r"F:\zzzzzzzzzzzzzzzzzzzzzzzzzz1", save_df_to=r"F:\saveto"
# )
# search_folder.create_flatcopy_link(separator="Ç", saveto=r"F:\symlinks")
# search_folder.create_simlink_in_folder(filtered_df=search_folder.df, printresult=True)
# search_folder.create_flatcopy_link(separator="#", saveto=r"F:\symlinks")
# search_folder.flatcopyfiles(filtered_df=search_folder.df, printresult=True)
# all_txt_files = search_folder.df.loc[search_folder.df.f_filepath.str.contains("\.txt$")].copy()
# searchresultsdf = search_folder.search_with_regex_in_files(
#     regular_expression=r"[^\n]+Bilderraten[^\n]+",
#     df=all_txt_files,
#     ignorecase=False,
#     dotall=False,
#     printresult=True,
#     use_bs4=True,
# )
# search_folder.printdf(start=1, how_many_lines=1000)
# search_folder.delete_files(filtered_df=all_txt_files, printresult=True, ask_before=True)
