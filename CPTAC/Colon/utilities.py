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

import pandas as pd
import numpy as np

class Utilities:
    def __init__(self):
        pass

#    def compare_gene(self, df1, df2, gene):
#        """
#        Parameters
#        df1: omics dataframe (proteomics) to be selected from
#        df2: other omics dataframe (transcriptomics) to be selected from
#        gene: gene to select from each of the dataframes
#
#        Returns
#        Dataframe containing two columns. Each column is the data for the specified gene from the two specified dataframes
#        """
#        if (type(df1) != pd.DataFrame) or (type(df2) != pd.DataFrame):
#            print("Provided data not a dataframe, please check that both data inputs are dataframes")
#            return
#        if gene in df1.columns and gene in df2.columns: #check provided gene is in both provided dataframes
#            common = df1.index.intersection(df2.index) #get rows common to df1 and df2
#            df1Matched = df1.loc[common] #select all common rows in df1
#            df1Matched = df1Matched.sort_index() #sort rows in ascending order
#            df2Matched = df2.loc[common] #select all common rows in df2
#            df2Matched = df2Matched.sort_index() #sort rows in ascending order
#            assert(hasattr(df1,"name")); assert(hasattr(df2,"name")) #check that both dataframes have a name, which is assigned at
#            dict = {df1.name:df1Matched[gene], df2.name:df2Matched[gene]} #create prep dictionary for dataframe mapping name to specified gene column
#            df = pd.DataFrame(dict, index = df1Matched.index) #create dataframe with common rows as rows, and dataframe name to specified gene column as columns
#            df.name = gene #dataframe is named as specified gene
#            return df
#        else:
#            if gene not in df1.columns:
#                if gene not in df2.columns:
#                    print(gene,"not found in either of the provided dataframes. Please check that the specified gene is included in both of the provided dataframes.")
#                else:
#                    print(gene, "not found in", df1.name, "dataframe. Please check that the specified gene is included in both of the provided dataframes.")
#            else:
#                if gene not in df2.columns:
#                    print(gene, "not found in", df2.name, "dataframe. Please check that the specified gene is included in both of the provided dataframes.")
#                else: #Shouldn't reach this branch
#                    print("Error asserting",gene,"in",df1.name,"and",df2.name,"dataframes.")
#
#    def compare_genes(self, df1, df2, genes):
#        """
#        Parameters
#        df1: omics dataframe (proteomics) to be selected from
#        df2: other omics dataframe (transcriptomics) to be selected from
#        genes: gene or list of genes to select from each of the dataframes
#
#        Returns
#        Dataframe containing columns equal to the number of genes provided times two. Each two-column set is the data for each specified gene from the two specified dataframes
#        """
#        if (type(df1) != pd.DataFrame) or (type(df2) != pd.DataFrame):
#            print("Provided data not a dataframe, please check that both data inputs are dataframes")
#            return
#        dfs = pd.DataFrame(index = df1.index.intersection(df2.index)) #create empty returnable dataframe with common rows of df1 and df2 as rows
#        for gene in genes: #loop through list of genes provided
#            df = Utilities().compare_gene(df1, df2, gene) #create temp dataframe per gene in list
#            new_col1 = df1.name + "_" + gene #create first new column using first dataframe name and gene
#            new_col2 = df2.name + "_" + gene #create second new column using second dataframe name and gene
#            df = df.rename(columns = {df1.name:new_col1, df2.name:new_col2}) #rename columns in returned dataframe
#            dfs = dfs.add(df, fill_value=0) #append temp dataframe onto returnable dataframe
#        dfs.name = str(len(genes)) + " Genes Combined" #Name returnable dataframe using number of genes provided
#        return dfs
#
#    def compare_clinical(self, clinical, data, clinical_col):
#        """
#        Parameters
#        clinical: clinical dataframe for omics data to be appended with
#        data: omics data for clinical data to be appended with
#        clinical_col: column in clinical dataframe to be inserted into provided omics data
#
#        Returns
#        Dataframe with specified column from clinical dataframe added to specified dataframe (i.e., proteomics) for comparison and easy plotting
#        """
#        if clinical_col in clinical:
#            df = data[data.columns] #new df variable prevents insert function overwriting the original data
#            df.insert(0, clinical_col, clinical[clinical_col]) #insert specified clinical column into specified omics data
#            df.name = data.name + " with " + clinical_col
#            return df
#        else:
#            print(clinical_col, "not found in clinical dataframe. You can check the available columns using get_clinical().columns")
#
#    def get_phosphosites(self, phosphoproteomics, gene):
#        """
#        Parameters
#        phosphoproteomics: the phosphoproteomics dataframe
#        gene: the gene we want to get the phosphosites for
#
#        Returns
#        dataframe containing the phosphosites for the specified gene
#        """
#        regex = gene + "_.*" #set regular expression using specified gene
#        phosphosites = phosphoproteomics.filter(regex = (regex)) #find all columns that match the regular expression, aka, all phosphosites for the specified gene
#        if len(phosphosites.columns) == 0:
#            print("Gene",gene, "not found in phosphoproteomics data")
#        phosphosites.name = 'phosphosites_{}'.format(gene)
#        return phosphosites
#
#    def compare_phosphosites(self, proteomics, phosphoproteomics, gene):
#        """
#        Parameters
#        proteomics: the proteomics dataframe
#        phosphoproteomics: the phosphoproteomics dataframe
#        gene: proteomics gene to query phosphoproteomics dataframe
#
#        Searches for any phosphosites on the gene provided
#
#        Returns
#        Dataframe with a column from proteomics for the gene specified, as well as columns for all phosphoproteomics columns beginning with the specified gene
#        """
#        if gene in proteomics.columns:
#            df = proteomics[[gene]] #select proteomics data for specified gene
#            phosphosites = self.get_phosphosites(phosphoproteomics, gene) #gets phosphosites for specified gene
#            if len(phosphosites.columns) > 0:
#                df = df.add(phosphosites, fill_value=0) #adds phosphosites columns to proteomics data for specified gene
#                df.name = gene + " proteomics and phosphoproteomics"
#                return df
#        else:
#            print(gene, "not found in proteomics dataframe. Available genes can be checked using get_proteomics().columns")

    def add_mutation_hierarchy(self, somatic): # private
        """
        Parameters
        somatic: somatic data to add mutation hierarchy to

        Returns
        Somatic mutation dataframe with added mutation hierarchy
        """
        mutation_hierarchy = {"nonsynonymous SNV":0,"nonframeshift deletion":0,"nonframeshift insertion":0,"nonframeshift substitution":0,"framshift substitution":1,"framshift insertion":1,"stopgain":1,"framshift deletion":1,"stoploss":1}
        hierarchy = []
        for x in somatic["Mutation"]: #for every value in the Mutation column, append its value in the hard coded mutation hierarchy
            if x in mutation_hierarchy.keys():
                hierarchy.append(mutation_hierarchy[x])
            else:
                hierarchy.append(float('NaN'))
        somatic = somatic.assign(Mutation_Hierarchy =  hierarchy)
        return somatic

#    def merge_somatic(self, somatic, gene, df_gene, multiple_mutations = False): # private
#        """
#        Parameters
#        somatic: somatic mutations dataframe that will be parsed for specified gene data
#        gene: string of gene to be selected for in somatic mutation data
#        df_gene: selection of omics data for particular gene to be merged with somatic data
#        multiple_mutations: boolean indicating whether to include multiple mutations for specified gene in an individual
#
#        Returns
#        Dataframe of merged somatic and omics dataframes based on gene provided
#        """
#        if sum(somatic["Gene"] == gene) > 0:
#            somatic_gene = somatic[somatic["Gene"] == gene] #select for all mutations for specified gene
#            somatic_gene = somatic_gene.drop(columns = ["Gene"]) #drop the gene column due to every value being the same
#            somatic_gene = somatic_gene.set_index("SampleID") #set index as SampleID
#            if not multiple_mutations:
#                somatic_gene = self.add_mutation_hierarchy(somatic_gene) #appends hierachy for sorting so correct duplicate can be kept
#                somatic_gene = somatic_gene.sort_values(by = ["SampleID","Mutation_Hierarchy"], ascending = [True,False]) #sorts by patient key, then by hierarchy so the duplicates will come with the higher number first
#                somatic_gene = somatic_gene[~somatic_gene.index.duplicated(keep="first")] #keeps first duplicate row if indices are the same
#            merge = df_gene.join(somatic_gene, how = "left") #left join omics data and mutation data (left being the omics data)
#            merge = merge.fillna(value = {'Mutation':"Wildtype"}) #fill in all Mutation NA values (no mutation data) as Wildtype
#            #merge["index"] = merge.index #set index values as column
#            merge = merge.assign(Sample_Status = np.where(merge.index.str[-1] != "N", "Tumor", "Normal")) #add patient type, setting all samples labels not ending in "N" as Tumor, others as normal. 
#            #merge["Sample_Status"] = np.nan # For now
#            merge.loc[merge.Sample_Status == "Normal","Mutation"] = "Wildtype_Normal" #change all Wildtype for Normal samples to Wildtype_Normal
#            merge.loc[merge.Mutation == "Wildtype","Mutation"] = "Wildtype_Tumor" #change all other Wildtype (should be for Tumor samples with imputed Wildtype value) to Wildtype_Tumor
#            merge = merge.fillna(value={'Location':'No_mutation'}) # If there's no location, there wasn't a mutation--make it easier for people to understand what that means.
#            merge.name = df_gene.columns[0] + " omics data with " + gene + " mutation data"
#            return merge
#        else:
#            print("Gene", gene, "not found in somatic mutations.")
#
#    def merge_mutations(self, omics, somatic, gene, duplicates = False):
#        """
#        Parameters
#        omics: dataframe containing specific omics data
#        somatic: dataframe of somatic mutation data
#        gene: string of specific gene to merge omics and somatic data on
#        duplicates: boolean value indicating whether to include duplicate gene mutations for an individual
#
#        Returns
#        Dataframe of merged omics and somatic data based on gene provided
#        """
#        if gene in omics.columns:
#            omics_gene_df = omics[[gene]] #select omics data for specified gene
#            if duplicates: #don't filter out duplicate sample mutations
#                return self.merge_somatic(somatic, gene, omics_gene_df, multiple_mutations = True)
#            else: #filter out duplicate sample mutations
#                merged_with_duplicates = self.merge_somatic(somatic, gene, omics_gene_df)
#                merged = merged_with_duplicates[[gene, "Mutation", "Sample_Status"]]
#                merged.name = merged_with_duplicates.name
#                return merged
#        elif omics.name.split("_")[0] == "phosphoproteomics":
#            phosphosites = self.get_phosphosites(omics, gene)
#            if len(phosphosites.columns) > 0:
#                if duplicates:#don't filter out duplicate sample mutations
#                    return self.merge_somatic(somatic, gene, phosphosites, multiple_mutations = True)
#                else:#filter out duplicate sample mutations
#                    columns = list(phosphosites.columns)
#                    columns.append("Mutation")
#                    columns.append("Sample_Status")
#                    merged_somatic_full = self.merge_somatic(somatic, gene, phosphosites)
#                    merged_somatic = merged_somatic_full[columns] #select all phosphosites, mutation, and patient type columns
#                    merged_somatic.name = merged_somatic_full.name
#                    return merged_somatic
#        else:
#            print("Gene", gene, "not found in", omics.name, "data")
#
#    def merge_mutations_trans(self, omics, omicsGene, somatic, somaticGene, duplicates = False):
#        """
#        Parameters
#        omics: dataframe containing specific omics data (i.e. proteomics, transcriptomics)
#        omicsGene: string of specific gene to merge from omics data
#        somatic: dataframe of somatic mutation data
#        somaticGene: string of specific gene to merge from somatic data
#        duplicates: boolean value indicating whether to include duplicate gene mutations for an individual
#
#        Returns
#        Dataframe of merged omics data (based on specific omicsGene) with somatic data (based on specific somaticGene)
#        """
#        merged_somatic = None
#        if omicsGene in omics.columns:
#            omics_gene_df = omics[[omicsGene]]
#            if duplicates:
#                merged_somatic = self.merge_somatic(somatic, somaticGene, omics_gene_df, multiple_mutations = True)
#            else:
#                merged_somatic_full = self.merge_somatic(somatic, somaticGene, omics_gene_df)
#                merged_somatic = merged_somatic_full[[omicsGene, "Mutation", "Sample_Status"]]
#                merged_somatic.name = merged_somatic_full.name
#        elif omics.name.split("_")[0] == "phosphoproteomics":
#            phosphosites = self.get_phosphosites(omics, omicsGene)
#            if len(phosphosites.columns) > 0:
#                if duplicates:
#                    merged_somatic = self.merge_somatic(somatic, somaticGene, phosphosites, multiple_mutations = True)
#                else:
#                    columns = list(phosphosites.columns)
#                    columns.append("Mutation")
#                    columns.append("Sample_Status")
#                    merged_somatic_full = self.merge_somatic(somatic, somaticGene, phosphosites)
#                    merged_somatic = merged_somatic_full[columns]
#                    merged_somatic.name = merged_somatic_full.name
#        else:
#            print("Gene", omicsGene, "not found in", omics.name,"data")
#            return
#        if merged_somatic is None:
#            return
#        merged_somatic = merged_somatic.rename(columns={omicsGene:omicsGene + '_omics', 'Mutation':somaticGene + '_Mutation', 'Location':somaticGene + '_Location', 'Sample_Status':somaticGene + '_Sample_Status'}) # Add the gene name to the column headers, so that it's clear which gene the data is for.
#        return merged_somatic

# Next 4 functions are for working with mutation data
    def get_mutations_for_gene(self, somatic, gene, multiple_mutations):
        """Gets all the mutations for a specific gene, for all patients.

        Parameters:
        somatic (pandas.core.frame.DataFrame): The somatic mutation dataframe that we'll grab the mutation data from.
        gene (str): The gene to grab mutations for.
        multiple_mutations (bool): Whether to keep multiple mutations on the gene for each patient, or only report the highest priority mutation per patient.

        Returns:
        pandas.core.frame.DataFrame: The mutations in each patient for the specified gene.
        """
        mutations = somatic[somatic["Gene"] == gene]

        if len(mutations) == 0: # If the gene doesn't match any in the dataframe, tell them, and return None.
            print("{} gene not found in somatic mutations data.".format(gene))
            return

        mutations = mutations.drop(columns=["Gene"]) # Drop the gene column due to every value being the same
        mutations = mutations.set_index("SampleID") # Set index as SampleID for merging
        if not multiple_mutations: # Filter out multiple mutations for a single sample
            mutations = self.add_mutation_hierarchy(mutations) # Appends hierachy for sorting so correct duplicate can be kept
            mutations = mutations.sort_values(by = ["SampleID","Mutation_Hierarchy"], ascending = [True,False]) # Sorts by patient key, then by hierarchy so the duplicates will come with the higher number first
            mutations = mutations[~mutations.index.duplicated(keep="first")] # Keeps first duplicate row if indices are the same
            mutations = mutations.drop(columns=['Mutation_Hierarchy']) # Drop the Mutation_Hierarchy now that we've dropped the duplicates

        mutations = mutations.rename(columns=lambda x:'{}_{}'.format(gene, x)) # Add the gene name to end beginning of each column header, to preserve info when we merge dataframes
        mutations.name = 'Somatic mutation data for {} gene'.format(gene)
        return mutations

    def get_mutations_for_genes(self, somatic, genes, multiple_mutations):
        """Gets all the mutations for a list of genes, for all patients.

        Parameters:
        somatic (pandas.core.frame.DataFrame): The somatic mutation dataframe that we'll grab the mutation data from.
        genes (list): The genes, as strings, to grab mutations for.
        multiple_mutations (bool): Whether to keep multiple mutations on a single gene for each patient, or only report the highest priority mutation per patient.

        Returns:
        pandas.core.frame.DataFrame: The mutations in each patient for the specified genes.
        """
        df = pd.DataFrame(index=somatic['SampleID'].drop_duplicates()) # Create an empty dataframe, which we'll fill with the columns we select using our genes, and then return.
        for gene in genes:
            selected = self.get_mutations_for_gene(somatic, gene, multiple_mutations) # Get the mutations for our gene
            if selected is None: # If there's no mutation data for that gene, get_mutations_for_gene will have printed an error message. Return None.
                return
            df = df.join(selected, how='left') # Otherwise, append the columns to our dataframe we'll return.
        df.name = "Somatic mutation data for {} genes".format(len(genes)) # Name the dataframe!
        return df

    def get_mutations_from_str_or_list(self, somatic, genes, multiple_mutations):
        """Determines whether you passed it a single gene or a list of genes, selects the corresponding mutations from the somatic mutation dataframe, and returns them.

        Parameters:
        somatic (pandas.core.frame.DataFrame): The somatic mutation dataframe we'll grab the mutation data from.
        genes (str or list): gene(s) to select mutations for. str if one gene, list if multiple.
        multiple_mutations (bool): Whether to keep multiple mutations on the gene for each patient, or only report the highest priority mutation per patient.

        Returns:
        pandas.core.frame.DataFrame: the mutation data corresponding to the gene(s), as a dataframe.
        """
        if isinstance(genes, str): # If it's a single gene, feed it to the proper function
            return self.get_mutations_for_gene(somatic, genes, multiple_mutations)
        elif isinstance(genes, list): # If it's a list of genes, feed it to the proper function
            return self.get_mutations_for_genes(somatic, genes, multiple_mutations)
        else: # If it's neither of those, they done messed up. Tell 'em.
            print("Genes parameter {} is of invalid type {}. Valid types: str or list.".format(genes, type(genes)))

    def append_mutations_to_omics(self, somatic, omics_df, mutation_genes, omics_genes, multiple_mutations, show_location):
        """Select all mutations for specified gene(s), and append to all or part of the given omics dataframe.

        Parameters:
        somatic (pandas.core.frame.DataFrame): Somatic mutation dataframe we'll get the dataframe.
        omics_df (pandas.core.frame.DataFrame): Omics dataframe to append the mutation data to.
        mutation_genes (str or list): The gene(s) to get mutation data for. str if one gene, list if multiple.
        omics_genes (str or list): Gene(s) to select from the omics dataframe. str if one gene, list if multiple. Passing None will select the entire omics dataframe.
        multiple_mutations (bool): Whether to keep multiple mutations on the gene for each patient, or only report the highest priority mutation per patient.
        show_location (bool): Whether to include the Location column from the mutation dataframe.

        Returns:
        pandas.core.frame.DataFrame: The mutations for the specified gene, appended to all or part of the omics dataframe.
        """
        omics = self.get_omics_from_str_or_list(omics_df, omics_genes)
        mutations = self.get_mutations_from_str_or_list(somatic, mutation_genes, multiple_mutations)

        if (omics is not None) and (mutations is not None): # If either selector returned None, then there were gene(s) that didn't match anything, and an error message was printed. We'll return None.
            merge = omics.join(mutations, how = "left") # Left join omics data and mutation data (left being the omics data)

            merge = merge.assign(Sample_Status = np.where(merge.index.str[-1] != "N", "Tumor", "Normal")) # Add sample status, setting all samples labels not ending in "N" as Tumor, others as normal. 

            mutation_regex = r'.*_Mutation' # Construct regex to find all mutation columns
            mutation_cols = [col for col in merge.columns.values if re.match(mutation_regex, col)] # Get a list of all mutation columns
            for mutation_col in mutation_cols:
                merge.loc[(merge['Sample_Status'] == "Normal") & (pd.isnull(merge[mutation_col])), mutation_col] = "Wildtype_Normal" # Change all NaN mutation values (i.e., no mutation data for that sample) for Normal samples to Wildtype_Normal
                merge.loc[(merge['Sample_Status'] == "Tumor") & (pd.isnull(merge[mutation_col])), mutation_col] = "Wildtype_Tumor" # Change all NaN mutation values (i.e., no mutation data for that sample) for Tumor samples to Wildtype_Tumor

            location_regex = r'.*_Location' # Construct regex to find all location columns
            location_cols = [col for col in merge.columns.values if re.match(location_regex, col)] # Get a list of all location columns
            for location_col in location_cols:
                if show_location:
                    merge = merge.fillna(value={location_col:'No_mutation'}) # If there's no location, there wasn't a mutation--make it easier for people to understand what that means.
                else:
                    merge = merge.drop(columns=[location_col]) # Drop the location column, if the caller wanted us to.

            merge.name = "{}, with {}".format(omics.name, mutations.name) # Give it a name identifying the data in it
            return merge

# Next 4 functions are for working with omics data
    def get_col_from_omics(self, omics_df, gene): # private
        """Based on a single gene, select a column or columns from an omics dataframe. If dataframe is phospho- or acetylproteomics, grabs all columns that match the gene.

        Parameters:
        omics_df (pandas.core.frame.DataFrame): omics dataframe to select colum(s) from.
        gene (str): gene to use to select column(s).

        Returns:
        pandas.core.frame.DataFrame: The selected column(s) from the dataframe.
        """
        if omics_df.name == ('phosphoproteomics_site' or 'acetylproteomics'):
            regex = gene + "_.*" # Build a regex to get all columns that match the gene
        else:
            regex = '^{}$'.format(gene)

        selected = omics_df.filter(regex = (regex)) # Find all columns that match the gene. If only one column matches, DataFrame.filter will still return a dataframe, not a series :)
        if len(selected.columns) == 0: # If none of the columns matched the gene, print an error message and return None.
            print('{} did not match any columns in {} dataframe. Please double check that it is included in the dataframe.'.format(gene, omics_df.name))
            return
        selected = selected.rename(columns=lambda x:'{}_{}'.format(x, omics_df.name)) # Append dataframe name to end of each column header, to preserve info when we merge dataframes
        selected.name = "{} for {}".format(omics_df.name, gene) # Give the dataframe a name!
        return selected

    def get_cols_from_omics(self, omics_df, genes): # private
        """Based on a list of genes, select multiple columns from an omics dataframe, and return the selected columns as one dataframe.

        Parameters:
        omics_df (pandas.core.frame.DataFrame): omics dataframe to select column(s) from.
        genes (list): list of genes, as strings, to use to select columns.

        Returns:
        pandas.core.frame.DataFrame: The selected columns from the dataframe.
        """
        df = pd.DataFrame(index=omics_df.index) # Create an empty dataframe, which we'll fill with the columns we select using our genes, and then return.
        for gene in genes:
            selected = self.get_col_from_omics(omics_df, gene) # Get the columns for that gene from the dataframe
            if selected is None: # If it didn't match any columns, get_col_from_omics will have printed an error message. Return None.
                return
            df = df.join(selected, how='left') # Otherwise, append the columns to our dataframe we'll return.
        df.name = "{} for {} genes".format(omics_df.name, len(genes)) # Name the dataframe!
        return df

    def get_omics_from_str_or_list(self, omics_df, genes):
        """Determines whether you passed it a single gene or a list of genes, selects the corresponding columns from the omics dataframe, and returns them.

        Parameters:
        omics_df (pandas.core.frame.DataFrame): omics dataframe to select columns from
        genes (str or list): gene(s) to use to select columns from omics_df. str if one gene, list if multiple. Passing None will select the entire omics dataframe.

        Returns:
        pandas.core.frame.DataFrame: the columns from omics_df corresponding to the gene(s), as a dataframe.
        """
        if isinstance(genes, str): # If it's a single gene, feed it to the proper function
            return self.get_col_from_omics(omics_df, genes)
        elif isinstance(genes, list): # If it's a list of genes, feed it to the proper function
            return self.get_cols_from_omics(omics_df, genes)
        elif genes is None: # If it's the default of None, rename columns and return the entire dataframe
            return_df = omics_df.rename(columns=lambda x:'{}_{}'.format(x, omics_df.name)) # Append dataframe name to end of each column header, to preserve info when we merge dataframes
            return_df.name = omics_df.name # Name the return dataframe
            return return_df
        else: # If it's none of those, they done messed up. Tell 'em.
            print("Genes parameter {} is of invalid type {}. Valid types: str, list, or NoneType.".format(genes, type(genes)))

    def compare_omics(self, df1, df2, genes1, genes2):
        """Select columns for one gene or a list of genes from one omics dataframe, and columns for another gene or list of genes from another omics dataframe, and join them into one dataframe.

        Parameters:
        df1 (pandas.core.frame.DataFrame): first omics dataframe to select from.
        genes1 (str or list): gene(s) for column(s) to select from the first omics dataframe. str if one gene, list of strings if multiple genes. Passing None will select the entire omics dataframe.
        df2 (pandas.core.frame.DataFrame): second omics dataframe to select from.
        genes2 (str or list): gene(s) for column(s) to select from the second omics dataframe. str if one gene, list of strings if multiple genes. Passing None will select the entire omics dataframe.

        Returns:
        pandas.core.frame.DataFrame: The data from the selected columns from the two dataframes, joined into one dataframe.
        """
        selected1 = self.get_omics_from_str_or_list(df1, genes1)
        selected2 = self.get_omics_from_str_or_list(df2, genes2)

        if (selected1 is not None) and (selected2 is not None): # If either selector returned None, the gene(s) didn't match any columns, and it printed an informative error message already. We'll return None.
            df = selected1.join(selected2, how='inner') # Join the rows common to both dataframes
            df = df.sort_index() # Sort rows in ascending order
            df.name = "{}, with {}".format(selected1.name, selected2.name) # Give it a nice name identifying the data in it.
            return df

# Next 4 functions are for working with clinical and derived molecular data
    def get_col_from_clinical(self, df, col):
        """Get a single column from the clinical or derived_molecular dataframe.

        Parameters:
        df (pandas.core.frame.DataFrame): The dataframe to select the column from. Either clinical or derived_molecular.
        col (str): The column to select from the dataframe.

        Returns:
        pandas.core.frame.DataFrame: The specified column from the given dataframe. We return it as a dataframe for easy merging later.
        """
        if col not in df.columns.values: # If they didn't give us one of the actual columns, tell them and return None.
            print('{} column not found in {} dataframe. Please double check that it is included in the dataframe.'.format(col, df.name))
            return

        selected = df.loc[:, [col]] # Select the column from the dataframe, keeping it as a dataframe
        selected.name = '{} from {}'.format(col, df.name) # Give it a name, identifying which dataframe it came from
        return selected

    def get_cols_from_clinical(self, df, cols):
        """Select several columns, given as a list, from either the clinical or derived_molecular dataframe.

        Parameters:
        df (pandas.core.frame.DataFrame): The dataframe to select the column from. Either clinical derived_molecular.
        cols (list): A list of the columns, as strings, to select from the dataframe.

        Returns:
        pandas.core.frame.DataFrame: The specified columns from the given dataframe.
        """
        return_df = pd.DataFrame(index=df.index) # Create an empty dataframe, which we'll fill with the columns we select, and then return.
        for col in cols:
            selected = self.get_col_from_clinical(df, col) # Get the columns from the given dataframe
            if selected is None: # If it didn't match any columns, get_col_from_omics will have printed an error message. Return None.
                return
            return_df = return_df.join(selected, how='left') # Otherwise, append the columns to our dataframe we'll return.
        return_df.name = "{} columns from {}".format(len(cols), df.name) # Name the dataframe!
        return return_df

    def get_clinical_from_str_or_list(self, df, cols):
        """Determines whether you passed it a single column or a list of columns, then selects them from the given dataframe, and returns them.

        Parameters:
        df (pandas.core.frame.DataFrame): The dataframe to select column(s) from. Either clinical or derived_molecular.
        cols (str or list): Column(s) to select from the dataframe. str if one, list if multiple.

        Returns:
        pandas.core.frame.DataFrame: The specificed columns from the given dataframe.
        """
        if isinstance(cols, str): # If it's a single column, feed it to the proper function
            return self.get_col_from_clinical(df, cols)
        elif isinstance(cols, list): # If it's a list of columns, feed it to the proper function
            return self.get_cols_from_clinical(df, cols)
        else: # If it's neither of those, they done messed up. Tell 'em.
            print("Columns parameter {} is of invalid type {}. Valid types: str or list.".format(cols, type(cols)))

    def append_clinical_to_omics(self, df, omics_df, df_cols, omics_cols):
        """Selected the specified columns from either the clinical or derived_molecular dataframe, and append to all or part of the given omics dataframe.

        Parameters:
        df (pandas.core.frame.DataFrame): Either the clinical or derived_molecular dataframe, from which we'll select our columns to append.
        omics_df (pandas.core.frame.DataFrame): The omics dataframe to append to.
        df_cols (str or list): Column(s) to select from the clinical or derived_molecular dataframe. str if one column, list of strings if multiple.
        omics_cols (str or list): Gene(s) to select data for from the omics dataframe. Passing None will select the entire omics dataframe.

        Returns:
        pandas.core.frame.DataFrame: The selected columns from the clinical or derived_molecular dataframe, appended to the selected columns from the omics dataframe.
        """
        df_selected = self.get_clinical_from_str_or_list(df, df_cols)
        omics_selected = self.get_omics_from_str_or_list(omics_df, omics_cols)

        if (df_selected is not None) and (omics_selected is not None): # If either selector returned None, the key(s) didn't match any columns, and it printed an informative error message already. We'll return None.
            df = df_selected.join(omics_selected, how='inner') # Join the rows common to both dataframes
            df = df.sort_index() # Sort rows in ascending order
            df.name = "{}, with {}".format(df_selected.name, omics_selected.name) # Give it a nice name identifying the data in it.
            return df
