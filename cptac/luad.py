#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import numpy as np
import pandas as pd
import os
from .dataset import DataSet
from .dataframe_tools import *
from .file_download import update_index
from .file_tools import validate_version, get_version_files_paths
from .dataframe_tools import *
from .exceptions import NoInternetError, FailedReindexWarning

# Comments beginning with "# FILL:" contain specific filling instructions.

class Luad(DataSet):

    def __init__(self, version="latest"):
        """Load all of the luad dataframes as values in the self._data dict variable, with names as keys, and format them properly."""

        # Call the parent DataSet __init__ function, which initializes self._data and other variables we need
        super().__init__("luad")

        # FILL: The following overloading may or not be needed for your dataset.
        # Overload the gene separator for column names in the phosphoproteomics dataframe. In the luad data, it's an underscore, not a dash like most datasets.
        #self._gene_separator = "_"

        # FILL: If needed, overload the self._valid_omics_dfs and self._valid_metadata_dfs variables that were initialized in the parent DataSet init.

        # Update the index, if possible. If there's no internet, that's fine.
        try:
            update_index(self._cancer_type)
        except NoInternetError:
            pass

        # Validate the version
        self._version = validate_version(version, self._cancer_type, use_context="init")

        # Get the paths to all the data files
        data_files = [
            "luad-v2.0-cnv-gene-LR.gct.gz",
            "luad-v2.0-phosphoproteome-ratio-norm-NArm.gct.gz",
            "luad-v2.0-proteome-ratio-norm-NArm.gct.gz",
            "luad-v2.0-rnaseq-circ-rna.csv.gz",
            "luad-v2.0-rnaseq-prot-uq-rpkm-log2-NArm-row-norm.gct.gz",
            "luad-v2.0-sample-annotation.csv.gz"]
        data_files_paths = get_version_files_paths(self._cancer_type, self._version, data_files)

        # Load the data into dataframes in the self._data dict
        loading_msg = "Loading dataframes"
        for file_path in data_files_paths: # Loops through files variable

            # Print a loading message. We add a dot every time, so the user knows it's not frozen.
            loading_msg = loading_msg + "."
            print(loading_msg, end='\r')

            path_elements = file_path.split(os.sep) # Get a list of the levels of the path
            file_name = path_elements[-1] # The last element will be the name of the file
            df_name = file_name.split(".")[0] # Our dataframe name will be the first section of file name (i.e. proteomics.txt.gz becomes proteomics)

            # FILL: Here, insert conditional statements to load all the data files as dataframes into the self._data dictionary. Consult existing datasets for examples.
            if file_name == "luad-v2.0-cnv-gene-LR.gct.gz":
                df = pd.read_csv(file_path, sep="\t", skiprows=2, dtype=object)
                gene_filter = df['Description'] != 'na'
                df = df[gene_filter]
                cols_to_drop = ["GeneID","Description"]
                df = df.drop(columns=cols_to_drop)
                df = df.set_index("id")
                df = df.apply(pd.to_numeric)
                df = df.transpose()
                df.index.name="Patient_ID"
                df.columns.name=None
                df=df.sort_index()
                self._data["CNV"] = df


            if file_name == "luad-v2.0-phosphoproteome-ratio-norm-NArm.gct.gz":
                df = pd.read_csv(file_path, sep="\t", skiprows=2, dtype=object)
                gene_filter = df['geneSymbol'] != 'na'
                df = df[gene_filter]
                sites = df['variableSites']
                sites = sites.str.replace(" ","")
                sites = sites.str.replace("(?![STYsty])[A-Z]\d*[a-z]", "", regex=True)
                sites = sites.str.replace('[a-z]',"")
                df['geneSymbol']= df['geneSymbol'].str.cat(sites, sep="-")
                df = df.set_index('geneSymbol')
                cols_to_drop = ['id', 'id.1', 'id.description', 'numColumnsVMsiteObserved', 'bestScore', 'bestDeltaForwardReverseScore', 'Best_scoreVML', 'Best_numActualVMSites_sty', 'Best_numLocalizedVMsites_sty', 'variableSites', 'sequence', 'sequenceVML', 'accessionNumber_VMsites_numVMsitesPresent_numVMsitesLocalizedBest_earliestVMsiteAA_latestVMsiteAA', 'protein_mw', 'species', 'speciesMulti', 'orfCategory', 'accession_number', 'accession_numbers', 'protein_group_num', 'entry_name', 'GeneSymbol']
                df = df.drop(columns=cols_to_drop)
                df = df.apply(pd.to_numeric)
                df = df.transpose()
                df.index.name="Patient_ID"
                df.columns.name =None
                self._data["phosphoproteomics"] = df



            if file_name == "luad-v2.0-proteome-ratio-norm-NArm.gct.gz":
                df = pd.read_csv(file_path, skiprows=2, sep='\t', dtype=object)
                gene_filter = df['geneSymbol'] != 'na'
                df = df[gene_filter]
                df = df.set_index('geneSymbol')
                cols_to_drop = ['id', 'id.1', 'id.description', 'numColumnsProteinObserved', 'numSpectraProteinObserved', 'protein_mw', 'percentCoverage', 'numPepsUnique', 'scoreUnique', 'species', 'orfCategory', 'accession_number', 'accession_numbers', 'subgroupNum', 'entry_name', 'GeneSymbol']
                df = df.drop(columns=cols_to_drop)
                df = df.apply(pd.to_numeric)
                df = df.transpose()
                df.index.name="patient_ID"
                df.columns.name=None
                self._data["proteomics"] = df


            if file_name == "luad-v2.0-rnaseq-prot-uq-rpkm-log2-NArm-row-norm.gct.gz":
                 df = pd.read_csv(file_path, sep="\t", skiprows=2, dtype=object)
                 gene_filter = df['geneSymbol'] != 'na'
                 df = df[gene_filter]
                 df = df.set_index('geneSymbol')
                 cols_to_drop = ['id', 'gene_id', 'gene_type', 'length']
                 df = df.drop(columns = cols_to_drop)
                 df = df.apply(pd.to_numeric)
                 df = df.transpose()
                 df.index.name = "patient_ID"
                 df.columns.name = None
                 df = df.sort_index()
                 self._data["transcriptomics"] = df


            if file_name == "luad-v2.0-sample-annotation.csv.gz":
                df = pd.read_csv(file_path, sep=",", dtype=object)
                filter = df['QC.status'] == "QC.pass" #There are some samples that are internal references. IRs are used for scaling purposes, and don't belong to a single patient, so we want to drop them.
                df = df[filter]
                df = df.drop(clumns="Sample.ID") #Get rid of the Sample.ID column becuase the same information is stored in "Participant" which is formatted the way we want.
                df = df.set_index("Participant")
                df.index.name="Patient_ID"
                df = df.rename(columns={"Type":"Sample_Tumor_Normal"})
                self._data["metadata"] = df


            


            if file_name == "luad-v2.0-rnaseq-circ-rna.csv.gz":
                df = pd.read_csv(file_path, sep=",", dtype=object)
                #Sample.ID is the sample id
                #The unique identifier from the gene is going to look something like this: circ_chr10_100260218_100262063_CWF19L1
                #The nucleotide coordinates can be found in junction.5 and junction.3
                #Junction.5 and Junciton.3 are the coordinates you are looking for it is the first base of the donor and last base of the acceptor, respectively.
                #THe gene name can be found in gene.3 and gene.5. When they are different you can concatenate them.

                #Where are the quantitative values?


        print(' ' * len(loading_msg), end='\r') # Erase the loading message
        formatting_msg = "Formatting dataframes..."
        print(formatting_msg, end='\r')

        # FILL: Here, write code to format your dataframes properly. Requirements:
        # - All dataframes must be indexed by Sample_ID, not Patient_ID.
        #     - This means that two samples from the same patient will have the same Patient_ID, but different Sample_ID numbers.
        #     - Sample_ID numbers must be of the format S***, e.g. S001, S028, S144
        #     - clinical dataframe must contain a Patient_ID column that contains the Patient_ID for each sample
        #     - If the data did not come indexed with Sample_ID numbers, look at the Ovarian dataset for an example of generating Sample_ID numbers and mapping them to Patient_ID numbers.
        #     - Note that most datasets are originally indexed with a patient id, which we rename as the case id, and has a format like C3N-00352.
        #         - If one patient provided both a normal and a tumor sample, those samples will have the same patient/case id. Therefore, before any joining or reindexing, prepend an 'N' to all normal sample case ids, based on the column in the clinical dataframe indicating which samples are tumor or normal. See existing datasets for examples of how to do this.
        #
        # - Each dataframe's name must match the format for that type of dataframe in all the other datasets.
        #     - E.g., if your binary mutations dataframe is named mutations_binary, you'd need to rename it to somatic_mutation_binary to match the other datasets' binary mutation dataframes.
        #
        # - If the new dataset has a dataframe not included in any other datasets, you must write a getter for it in the parent DataSet class, found in cptac/dataset.py, using the private method DataSet._get_dataframe
        #
        # - You'd also need to add the new dataframe's name to self._valid_omics_dfs if it's a valid omics df for the DataSet merge functions, or self._valid_metadata_dfs if it's a valid metadata df for DataSet.append_metadata_to_omics
        #     - Note that a dataframe with multiple rows for each sample, like the treatment dataframe in the Ovarian dataset, should not be a valid dataset for joining
        #
        # - If any dataframes are split between two files--such as one file for the tumor sample proteomics, and one file for the normal sample proteomics--they'll have been read into separate dataframes, and you need to merge those into one dataframe.
        #     - Make sure that samples coming from a normal file have an 'N' added to their Patient_ID numbers, to keep a record of which ones are normal samples.
        #
        # - If multiple dataframes are contained in one file--e.g. clinical and derived_molecular data are both in clinical.txt, as in Endometrial--separate them out here.
        #
        # - Make sure that column names are consistent--e.g., all Patient_ID columns should be labeled as such, not as Clinical_Patient_Key or Case_ID or something else. Rename columns as necessary to match this.
        #
        # - The clinical dataframe must contain a Sample_Tumor_Normal column, which contains either "Tumor" or "Normal" for each sample, according to its status.
        #
        # - Only the clinical dataframe should contain a Patient_ID column. The other dataframes should contain just a Sample_ID index, and the data.
        #
        # - The column axis of each dataframe should have None as the value of its .name attribute
        #
        # - The index of each dataframe should have "Sample_ID" as the value of its .name attribute, since that's what the index is.
        #
        # - Make sure to drop any excluded cases, as in Endometrial.
        #
        # - Make sure that in dataframes where each column header is the name of a gene, the columns are in alphabetical order.

        print(" " * len(formatting_msg), end='\r') # Erase the formatting message

        print("success")
