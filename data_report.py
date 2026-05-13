import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Préparation des données
    """)
    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(glob, pd):
    #data = pd.read_csv("Dataset/year_data/worldriskindex-2025.csv")
    metadata = pd.read_excel("Dataset/metadata.xlsx")

    all_files = glob.glob('Dataset/year_data/*.csv')
    df_list = []

    import re #regular expression

    for f in all_files:
        temp_df = pd.read_csv(f)
        year_match = re.search(r'(\d{4})', f)
        if year_match:
            temp_df['Year'] = int(year_match.group(1))

        #Standardize column names
        if 'WRI.Country' in temp_df.columns:
            temp_df.rename(columns={'WRI.Country': 'Country'}, inplace=True)
        if 'ISO3' in temp_df.columns:
            temp_df.rename(columns={'ISO3': 'ISO3.Code'}, inplace=True)

        df_list.append(temp_df)

    df_temp = pd.concat(df_list, axis=0, ignore_index=True)
    return df_temp, metadata


@app.cell
def _(df_temp):
    df_temp.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Problème: les données sont peu visibles et accessibles pour un travail direct à la source.
    Solution:
    - Renommer les colonnes
    - Fusionner les colonnes similaires ou les déplacer dans un autre jeu de données pour jointure si besoin.
    """)
    return


@app.cell
def _(metadata):
    metadata
    return


@app.cell
def _(df, metadata):
    metadata_codes = metadata["Code"]
    metadata_codes

    data_columns = df.columns

    non_matching_columns = set(data_columns) - set(metadata_codes)
    non_matching_columns = [col for col in non_matching_columns if col[-4:] != "Norm" and col[-4:] != "Base" and col != "Year" ]

    non_matching_columns
    return (non_matching_columns,)


@app.cell
def _(non_matching_columns):
    [col for col in non_matching_columns if col[-4:] != "Norm" and col[-4:] != "Base"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut voir qu'il y a seulement les colonnes Country, Year et Country code (ISO code) qui ne sont pas présentes dans à la fois dans metadata et dans le jeu de données principal. On en déduit donc que toutes les colonnes du jeu de données sont expliquées dans metadata et seront donc, utilisables.
    """)
    return


@app.cell
def _(metadata):
    metadata[["Variable", "Code"]]
    return


@app.cell
def _(df_temp):
    df_temp[["EI_01b_Base", "EI_01a_Norm"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut voir que chaque colonne de résultat contient à la fois les données non retouchées et les données normalisées.
    On a deux types de format:
    - Données BASE: pourcentage ou par défaut
    - Données NORMALISEES: où toutes les valeurs se basent sur la valeur la plus grande.
    """)
    return


@app.cell
def _(df_temp):
    df_temp[["EI_01b_Base", "EI_01a_Base"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut constater une duplication de colonnes avec un contexte différent (ex: EI_01a, EI01c où l'intensité passe de fort à sévère)
    """)
    return


@app.cell
def _(df_temp):
    df = df_temp.rename(columns={
        "Country": "Pays",
        "ISO3.Code": "Code",
        "W": "Risque global",
        "E": "E_Exposition",
        "V": "V_Vulnérabilité",
        "S": "S_Susceptibilité",
        "C": "C_Adaptation court-terme",
        "A": "A_Adaptation long-terme",
        "S_01": "S_Développement SES",
        "S_02": "S_Manques SES",
        "S_03": "S_Inégalités sociétales",
        "S_04": "S_Touchés par violence conflits et catastrophes",
        "S_05": "S_Touchés par épidémies et maladies",
        "C_01": "C_Chocs sociétaux récents",
        "C_02": "C_Etat et gouvernements",
        "C_03": "C_Santé",
        "A_01": "A_Recherche et éducation",
        "A_02": "A_Vie longue et déprivations",
        "A_03": "A_Investissements",
        "EI_01": "E_Séismes",
        "EI_02": "E_Tsunamis",
        "EI_03": "E_Inondations côtes",
        "EI_04": "E_Inondations rivières",
        "EI_05": "E_Cyclones",
        "EI_06": "E_Sécheresses",
        "EI_07": "E_Montées des eaux",
        "SI_01": "S_Durée de vie",
        "SI_02": "S_Education",
        "SI_03": "S_Revenu",
        "SI_04": "S_Indépendance aides",
        "SI_05": "S_Manque infrastructures",
        "SI_06": "S_Manque énergie",
        "SI_07": "S_Manque IT",
        "SI_08": "S_Manque agriculture",
        "SI_09": "S_Disparités économiques",
        "SI_10": "S_Disparités démographiques",
        "SI_11": "S_Disparités genres",
        "SI_12": "Refugiés et déplacés",
        "SI_13": "S_Déplacés catastrophes",
        "SI_14": "S_Déplacés conflits",
        "CI_01": "C_Chocs sociétaux catastrophes",
        "CI_02": "C_Chocs sociétaux conflits",
        "CI_03": "C_Indicateur démocratique",
        "CI_04": "C_Responsabilité gouvernementale",
        "CI_05": "C_Personnel médical",
        "CI_06": "C_Structures médicales",
        "CI_07": "C_Mortalité",
        "AI_01": "A_Education",
        "AI_02": "A_Recherche",
        "AI_03": "A_Déprivations long-terme",
        "AI_04": "A_Santé long terme",

        "AI_01a_Base": "A_B_UsdPP scolaires par personne",
        "AI_01a_Norm": "A_N_UsdPP scolaires par personne",
        "AI_01b_Base": "A_B_Nb professeurs scolaires",
        "AI_01b_Norm": "A_N_Nb professeurs scolaires",
        "AI_01c_Base": "A_B_UsdPP inscription scolaires",
        "AI_01c_Norm": "A_N_UsdPP inscription scolaires",

        "AI_02a_Base": "A_B_UsdPP R&D par personne",
        "AI_02a_Norm": "A_N_UsdPP R&D par personne",
        "AI_02b_Base": "A_B_Nb personnel R&D",
        "AI_02b_Norm": "A_N_Nb personnel R&D",
        "AI_02c_Base": "A_B_UsdPP inscription sup",
        "AI_02c_Norm": "A_N_UsdPP inscription sup",

        "AI_03a_Base": "A_B_Décès par sources eau",
        "AI_03a_Norm": "A_N_Décès par sources eau",
        "AI_03b_Base": "A_B_Décès par pollution air",
        "AI_03b_Norm": "A_N_Décès par pollution air",
        "AI_03c_Base": "A_B_Décès par malnutrition maternelle",
        "AI_03c_Norm": "A_N_Décès par malnutrition maternelle",

        "AI_04a_Base": "A_B_Pct enfants vaccinés DTP",
        "AI_04a_Norm": "A_N_Pct enfants vaccinés DTP",
        "AI_04b_Base": "A_B_Pct enfants vaccinés Polio",
        "AI_04b_Norm": "A_N_Pct enfants vaccinés Polio",
        "AI_04c_Base": "A_B_Pct enfants vaccinés MMR",
        "AI_04c_Norm": "A_N_Pct enfants vaccinés MMR",

        "AI_05a_Base": "A_B_UsdPP FBCF par personne",
        "AI_05a_Norm": "A_N_UsdPP FBCF par personne",
        "AI_05b_Base": "A_B_Pct instabilités prix consommation",
        "AI_05b_Norm": "A_N_Pct instabilités prix consommation",

        "CL_01a_Base": "C_B_Nb personnes touchées par catastrophe",
        "CL_01a_Norm": "C_N_Nb personnes touchées par catastrophe",
        "CL_01b_Base": "C_B_Pct personnes touchées par catastrophe",
        "CL_01b_Norm": "C_N_Pct personnes touchées par catastrophe",

        "CL_02a_Base": "C_B_Nb personnes tuées par conflits",
        "CL_02a_Norm": "C_N_Nb personnes tuées par conflits",
        "CL_02b_Base": "C_B_Pct personnes tuées par conflits",
        "CL_02b_Norm": "C_N_Pct personnes tuées par conflits",

        "CL_03a_Base": "C_B_Ind corruption",
        "CL_03a_Norm": "C_N_Ind corruption",
        "CL_03b_Base": "C_B_Ind application lois",
        "CL_03b_Norm": "C_N_Ind application lois",

        "CL_04a_Base": "C_B_Ind efficacité gouvernementale",
        "CL_04a_Norm": "C_N_Ind efficacité gouvernementale",
        "CL_04b_Base": "C_B_Ind stabilité politique et abs terreur",
        "CL_04b_Norm": "C_N_Ind stabilité politique et abs terreur",

        "CL_05a_Base": "C_B_PrsnPar1kPrsn practiciens médicaux",
        "CL_05a_Norm": "C_N_PrsnPar1kPrsn practiciens médicaux",
        "CL_05b_Base": "C_B_PrsnPar1kPrsn sage-femmes infirmiers",
        "CL_05b_Norm": "C_N_PrsnPar1kPrsn sage-femmes infirmiers",

        "CL_06a_Base": "C_B_UPar1kPrsn lits hôpitaux",
        "CL_06a_Norm": "C_N_UPar1kPrsn lits hôpitaux",
        "CL_06b_Base": "C_B_UsdPP dépenses santé",
        "CL_06b_Norm": "C_N_UsdPP dépenses santé",

        "CL_07a_Base": "C_B_DPar100kNés mortalité maternelle",
        "CL_07a_Norm": "C_N_DPar100kNés mortalité maternelle",
        "CL_07b_Base": "C_B_DPar100kNés mortalité infantile",
        "CL_07b_Norm": "C_N_DPar100kNés mortalité infantile",

        "SL_01a_Base": "S_B_Durée de vie naissance",
        "SL_01a_Norm": "S_N_Durée de vie naissance",
        "SL_01b_Base": "S_B_Durée de vie à 70 ans",
        "SL_01b_Norm": "S_N_Durée de vie à 70 ans",

        "SL_02a_Base": "S_B_Avg années scolarité",
        "SL_02a_Norm": "S_N_Avg années scolarité",
        "SL_02b_Base": "S_B_Durée scolaire estimée",
        "SL_02b_Norm": "S_N_Durée scolaire estimée",

        "SL_03a_Base": "S_B_UsdPP Revenu par habitant",
        "SL_03a_Norm": "S_N_UsdPP Revenu par habitant",
        "SL_03b_Base": "S_B_UsdPP Epargne par habitant",
        "SL_03b_Norm": "S_N_UsdPP Epargne par habitant",

        "SL_04a_Base": "S_B_UsdPP Aides officielles",
        "SL_04a_Norm": "S_N_UsdPP Aides officielles",
        "SL_04b_Base": "S_B_UsdPP Aides ponctuelles",
        "SL_04b_Norm": "S_N_UsdPP Aides ponctuelles",

        "SL_05a_Base": "S_B_Pct Accès eau potable",
        "SL_05a_Norm": "S_N_Pct Accès eau potable",
        "SL_05b_Base": "S_B_Pct Accès sanitaires",
        "SL_05b_Norm": "S_N_Pct Accès sanitaires",

        "SL_06a_Base": "S_B_Pct Accès électricité",
        "SL_06a_Norm": "S_N_Pct Accès électricité",
        "SL_06b_Base": "S_B_Pct Accès combustibles cuisine",
        "SL_06b_Norm": "S_N_Pct Accès combustibles cuisine",

        "SL_07a_Base": "S_B_UPar1kPrsn Souscriptions fibre",
        "SL_07a_Norm": "S_N_UPar1kPrsn Souscriptions fibre",
        "SL_07b_Base": "S_B_UPar1kPrsn Souscription téléphonie",
        "SL_07b_Norm": "S_N_UPar1kPrsn Souscription téléphonie",

        "SL_08a_Base": "S_B_Pct Prévalence sous-nutrition",
        "SL_08a_Norm": "S_N_Pct Prévalence sous-nutrition",
        "SL_08b_Base": "S_B_Pct Couverture besoins caloriques",
        "SL_08b_Norm": "S_N_Pct Couverture besoins caloriques",

        "SL_09a_Base": "S_B_GiniInd Revenus avant taxe",
        "SL_09a_Norm": "S_N_GiniInd Revenus avant taxe",
        "SL_09b_Base": "S_B_Ind Revenus top-down décile après taxe",
        "SL_09b_Norm": "S_N_GiniInd Revenus top-down décile après taxe",

        "SL_10a_Base": "S_B_Ind dépendance jeunes",
        "SL_10a_Norm": "S_N_Ind dépendance jeunes",
        "SL_10b_Base": "S_B_Ind dépendance âgés",
        "SL_10b_Norm": "S_N_Ind dépendance âgés",

        "SL_11a_Base": "S_B_Ind disparités genres fertilité adolescente",
        "SL_11a_Norm": "S_N_Ind disparités genres fertilité adolescente",
        "SL_11b_Base": "S_B_Ind disparités genres éducation",
        "SL_11b_Norm": "S_N_Ind disparités genres éducation",
        "SL_11c_Base": "S_B_Ind disparités genre éducation attendue",
        "SL_11c_Norm": "S_N_Ind disparités genre éducation attendue",
        "SL_11d_Base": "S_B_Ind disparités genres emploi",
        "SL_11d_Norm": "S_N_Ind disparités genres emploi",

        "SL_12a_Base": "S_B_Nb réfugiés et déplacés",
        "SL_12a_Norm": "S_N_Nb réfugiés et déplacés",
        "SL_12b_Base": "S_B_Pct réfugiés et déplacés",
        "SL_12b_Norm": "S_N_Pct réfugiés et déplacés",

        "SL_13a_Base": "S_B_Nb déplacés par catastrophes",
        "SL_13a_Norm": "S_N_Nb déplacés par catastrophes",
        "SL_13b_Base": "S_B_Pct déplacés par catastrophes",
        "SL_13b_Norm": "S_N_Pct déplacés par catastrophes",

        "SL_14a_Base": "S_B_Nb déplacés par conflits",
        "SL_14a_Norm": "S_N_Nb déplacés par conflits",
        "SL_14b_Base": "S_B_Pct déplacés par conflits",
        "SL_14b_Norm": "S_N_Pct déplacés par conflits",

        "SL_15a_Base": "S_B_CasPar1kPrsn prévalences Sida",
        "SL_15a_Norm": "S_N_CasPar1kPrsn prévalences Sida",
        "SL_15b_Base": "S_B_CasPar1kPrsn prévalences tuberculose et respiratoires",
        "SL_15b_Norm": "S_N_CasPar1kPrsn prévalences tuberculose et respiratoires",
        "SL_15c_Base": "S_B_CasPar1kPrsn prévalences Paludisme et maladies tropicales",
        "SL_15c_Norm": "S_N_CasPar1kPrsn prévalences Paludisme et maladies tropicales",
        "SL_15d_Base": "S_B_CasPar1kPrsn prévalences autres maladies infectieuses",
        "SL_15d_Norm": "S_N_CasPar1kPrsn prévalences autres maladies infectieuses",

        "EI_01a_Norm": "E_N_Avg population séismes haute intensité",
        "EI_01a_Base": "E_B_Avg population séismes haute intensité",
        "EI_01b_Norm": "E_N_Pct population séismes haute intensité",
        "EI_01b_Base": "E_B_Pct population séismes haute intensité",
        "EI_01c_Norm": "E_N_Avg population séismes sévère intensité",
        "EI_01c_Base": "E_B_Avg population séismes sévère intensité",
        "EI_01d_Norm": "E_N_Pct population séismes sévère intensité",
        "EI_01d_Base": "E_B_Pct population séismes sévère intensité",
        "EI_01e_Norm": "E_N_Avg population séismes extrême intensité",
        "EI_01e_Base": "E_B_Avg population séismes extrême intensité",
        "EI_01f_Norm": "E_N_Pct population séismes extrême intensité",
        "EI_01f_Base": "E_B_Pct population séismes extrême intensité",

        "EI_02a_Norm": "E_N_Avg population tsunamis haute intensité",
        "EI_02a_Base": "E_B_Avg population tsunamis haute intensité",
        "EI_02b_Norm": "E_N_Pct population tsunamis haute intensité",
        "EI_02b_Base": "E_B_Pct population tsunamis haute intensité",
        "EI_02c_Norm": "E_N_Avg population tsunamis sévère intensité",
        "EI_02c_Base": "E_B_Avg population tsunamis sévère intensité",
        "EI_02d_Norm": "E_N_Pct population tsunamis sévère intensité",
        "EI_02d_Base": "E_B_Pct population tsunamis sévère intensité",
        "EI_02e_Norm": "E_N_Avg population tsunamis extrême intensité",
        "EI_02e_Base": "E_B_Avg population tsunamis extrême intensité",
        "EI_02f_Norm": "E_N_Pct population tsunamis extrême intensité",
        "EI_02f_Base": "E_B_Pct population tsunamis extrême intensité",

        "EI_03a_Norm": "E_N_Avg population inondations côtes haute intensité",
        "EI_03a_Base": "E_B_Avg population inondations côtes haute intensité",
        "EI_03b_Norm": "E_N_Pct population inondations côtes haute intensité",
        "EI_03b_Base": "E_B_Pct population inondations côtes haute intensité",
        "EI_03c_Norm": "E_N_Avg population inondations côtes sévère intensité",
        "EI_03c_Base": "E_B_Avg population inondations côtes sévère intensité",
        "EI_03d_Norm": "E_N_Pct population inondations côtes sévère intensité",
        "EI_03d_Base": "E_B_Pct population inondations côtes sévère intensité",
        "EI_03e_Norm": "E_N_Avg population inondations côtes extrême intensité",
        "EI_03e_Base": "E_B_Avg population inondations côtes extrême intensité",
        "EI_03f_Norm": "E_N_Pct population inondations côtes extrême intensité",
        "EI_03f_Base": "E_B_Pct population inondations côtes extrême intensité",

        "EI_04a_Norm": "E_N_Avg population inondations rivières haute intensité",
        "EI_04a_Base": "E_B_Avg population inondations rivières haute intensité",
        "EI_04b_Norm": "E_N_Pct population inondations rivières haute intensité",
        "EI_04b_Base": "E_B_Pct population inondations rivières haute intensité",
        "EI_04c_Norm": "E_N_Avg population inondations rivières sévère intensité",
        "EI_04c_Base": "E_B_Avg population inondations rivières sévère intensité",
        "EI_04d_Norm": "E_N_Pct population inondations rivières sévère intensité",
        "EI_04d_Base": "E_B_Pct population inondations rivières sévère intensité",
        "EI_04e_Norm": "E_N_Avg population inondations rivières extrême intensité",
        "EI_04e_Base": "E_B_Avg population inondations rivières extrême intensité",
        "EI_04f_Norm": "E_N_Pct population inondations rivières extrême intensité",
        "EI_04f_Base": "E_B_Pct population inondations rivières extrême intensité",

        "EI_05a_Norm": "E_N_Avg population cyclones haute intensité",
        "EI_05a_Base": "E_B_Avg population cyclones haute intensité",
        "EI_05b_Norm": "E_N_Pct population cyclones haute intensité",
        "EI_05b_Base": "E_B_Pct population cyclones haute intensité",
        "EI_05c_Norm": "E_N_Avg population cyclones sévère intensité",
        "EI_05c_Base": "E_B_Avg population cyclones sévère intensité",
        "EI_05d_Norm": "E_N_Pct population cyclones sévère intensité",
        "EI_05d_Base": "E_B_Pct population cyclones sévère intensité",
        "EI_05e_Norm": "E_N_Avg population cyclones extrême intensité",
        "EI_05e_Base": "E_B_Avg population cyclones extrême intensité",
        "EI_05f_Norm": "E_N_Pct population cyclones extrême intensité",
        "EI_05f_Base": "E_B_Pct population cyclones extrême intensité",

        "EI_06a_Norm": "E_N_Avg population sécheresses haute intensité",
        "EI_06a_Base": "E_B_Avg population sécheresses haute intensité",
        "EI_06b_Norm": "E_N_Pct population sécheresses haute intensité",
        "EI_06b_Base": "E_B_Pct population sécheresses haute intensité",
        "EI_06c_Norm": "E_N_Avg population sécheresses sévère intensité",
        "EI_06c_Base": "E_B_Avg population sécheresses sévère intensité",
        "EI_06d_Norm": "E_N_Pct population sécheresses sévère intensité",
        "EI_06d_Base": "E_B_Pct population sécheresses sévère intensité",
        "EI_06e_Norm": "E_N_Avg population sécheresses extrême intensité",
        "EI_06e_Base": "E_B_Avg population sécheresses extrême intensité",
        "EI_06f_Norm": "E_N_Pct population sécheresses extrême intensité",
        "EI_06f_Base": "E_B_Pct population sécheresses extrême intensité",

        "EI_07a_Norm": "E_N_Nb population montée des eaux",
        "EI_07a_Base": "E_B_Nb population montée des eaux",
        "EI_07b_Norm": "E_N_Pct population montée des eaux",
        "EI_07b_Base": "E_B_Pct population montée des eaux",

        "SI_01a_Norm": "S_N_Y Durée vie à naissance",
        "SI_01a_Base": "S_B_Y Durée vie à naissance",
        "SI_01b_Norm": "S_N_Y Durée vie à 70y",
        "SI_01b_Base": "S_B_Y Durée vie à 70y",

        "SI_02a_Norm": "S_N_Y Durée moyenne école",
        "SI_02a_Base": "S_B_Y Durée moyenne école",
        "SI_02b_Norm": "S_N_Y Durée école primaire à tertiaire",
        "SI_02b_Base": "S_B_Y Durée école primaire à tertiaire",

        "SI_03a_Norm": "S_N_Sc RNB par habitant",
        "SI_03a_Base": "S_B_Sc RNB par habitant",
        "SI_03b_Norm": "S_N_Sc Epargne brute par habitant",
        "SI_03b_Base": "S_B_Sc Epargne brute par habitant",

        "SI_04a_Norm": "S_N_Nb volume aides officielles par habitant",
        "SI_04a_Base": "S_B_Nb volume aides officielles par habitant",
        "SI_04b_Norm": "S_N_Nb volume aides intermittence par habitant",
        "SI_04b_Base": "S_B_Nb volume aides intermittence par habitant",

        "SI_05a_Norm": "S_N_Pct accès eau",
        "SI_05a_Base": "S_B_Pct accès eau",
        "SI_05b_Norm": "S_N_Pct accès ordures",
        "SI_05b_Base": "S_B_Pct accès ordures",

        "SI_06a_Norm": "S_N_Pct accès électricité",
        "SI_06a_Base": "S_B_Pct accès électricité",
        "SI_06b_Norm": "S_N_Pct accès combustibles cuisine",
        "SI_06b_Base": "S_B_Pct accès combustibles cuisine",

        "SI_07a_Norm": "S_N_UP1kP Abonnement internet",
        "SI_07a_Base": "S_B_UP1kP Abonnement internet",
        "SI_07b_Norm": "S_N_UP1kP Abonnement téléphonique",
        "SI_07b_Base": "S_B_UP1kP Abonnement téléphonique",

        "SI_08a_Norm": "S_N_Pct Sous-nutrition",
        "SI_08a_Base": "S_B_Pct Sous-nutrition",
        "SI_08b_Norm": "S_N_Pct apport énergétique alimentaire",
        "SI_08b_Base": "S_B_Pct apport énergétique alimentaire",

        "SI_09a_Norm": "S_N_Sc Coef Gini avant impôts",
        "SI_09a_Base": "S_B_Sc Coef Gini avant impôts",
        "SI_09b_Norm": "S_N_Sc Rapport entre revenu déciles sup et inf avant impôts",
        "SI_09b_Base": "S_B_Sc Rapport entre revenu déciles sup et inf avant impôts",

        "SI_10a_Norm": "S_N_Sc Dépendance jeune âge",
        "SI_10a_Base": "S_B_Sc Dépendance jeune âge",
        "SI_10b_Norm": "S_N_Sc Dépendance âgé",
        "SI_10b_Base": "S_B_Sc Dépendance âgé",
        "SI_10_Norm": "S_N_Sc Dépendances âges",
        "SI_10_Base": "S_B_Sc Dépendances âges",

        "SI_11a_Norm": "S_N_Sc: Disparités genre adolescence",
        "SI_11a_Base": "S_B_Sc: Disparités genre adolescence",
        "SI_11b_Norm": "S_N_Sc: Disparités années école",
        "SI_11b_Base": "S_B_Sc: Disparités années école",
        "SI_11c_Norm": "S_N_Sc: Disparités années primaire vers tertiaire",
        "SI_11c_Base": "S_B_Sc: Disparités années primaire vers tertiaire",
        "SI_11_Norm": "S_N_Sc Disparités démographiques",

        "SI_12a_Norm": "S_N_Nb Réfugiés",
        "SI_12a_Base": "S_B_Nb Réfugiés",
        "SI_12b_Norm": "S_N_Pct Réfugiés",
        "SI_12b_Base": "S_B_Pct Réfugiés",

        "SI_13a_Norm": "S_N_Nb Déplacés cause sinistres",
        "SI_13a_Base": "S_B_Nb Déplacés cause sinistres",
        "SI_13b_Norm": "S_N_Pct Déplacés cause sinistres",
        "SI_13b_Base": "S_B_Pct Déplacés cause sinistres",

        "SI_14a_Norm": "S_N_Nb Déplacés cause violences",
        "SI_14a_Base": "S_B_Nb Déplacés cause violences",
        "SI_14b_Norm": "S_N_Pct Déplacés cause violences",
        "SI_14b_Base": "S_B_Pct Déplacés cause violences",

        "SI_15a_Norm": "S_N_CasPar100kPrsn Prévalence HIV",
        "SI_15a_Base": "S_B_CasPar100kPrsn Prévalence HIV",
        "SI_15b_Norm": "S_N_CasPar100kPrsn Prévalence Tuberculose et Respiratoires",
        "SI_15b_Base": "S_B_CasPar100kPrsn Prévalence Tuberculose et Respiratoires",
        "SI_15c_Norm": "S_N_CasPar100kPrsn Prévalence Tropicales et Malaria",
        "SI_15c_Base": "S_B_CasPar100kPrsn Prévalence Tropicales et Malaria",
        "SI_15d_Norm": "S_N_CasPar100kPrsn Prévalence Infections",
        "SI_15d_Base": "S_B_CasPar100kPrsn Prévalence Infections",

        "CI_01a_Norm": "C_N_Nb Population touchée sinistres 5 dernières années",
        "CI_01a_Base": "C_B_Nb Population touchée sinitres 5 dernières années",
        "CI_01b_Norm": "C_N_Pct Population touchée sinistres 5 dernières années",
        "CI_01b_Base": "C_B_Pct Population touchée sinistres 5 dernières années",

        "CI_02a_Norm": "C_N_Nb Population tuée conflits 5 dernières années",
        "CI_02a_Base": "C_B_Nb Population tuée conflits 5 dernières années",
        "CI_02b_Norm": "C_N_Avg Population tuée conflits 5 dernières années",
        "CI_02b_Base": "C_B_Avg Population tuées conflits 5 dernières années",

        "CI_03a_Norm": "C_N_Sc Contrôle corruption",
        "CI_03a_Base": "C_B_Sc Contrôle corruption",
        "CI_03b_Norm": "C_N_Sc Respect règles",
        "CI_03b_Base": "C_B_Sc Respect règles",

        "CI_04a_Norm": "C_N_Sc Efficacité gouvernementale",
        "CI_04a_Base": "C_B_Sc Efficacité gouvernementale",
        "CI_04b_Norm": "C_N_Sc Stabilité politique",
        "CI_04b_Base": "C_B_Sc Stabilité politique",

        "CI_05a_Norm": "C_N_PP1kP Docteurs et practiciens",
        "CI_05a_Base": "C_B_PP1kP Docteurs et practiciens",
        "CI_05b_Norm": "C_N_PP1kP Infirmiers et sage-femmes",
        "CI_05b_Base": "C_B_PP1kP Infirmiers et sage-femmes",

        "CI_06a_Norm": "C_N_UP1kP Lits d'hôpitaux",
        "CI_06a_Base": "C_B_UP1kP Lits d'hôpitaux",
        "CI_06b_Norm": "C_N_UsdPP Dépenses hospitalières par personne",
        "CI_06b_Base": "C_B_UsdPP Dépenses hospitalières par personne",

        "CI_07a_Norm": "C_N_Dp100kB Taux mortalité maternelle",
        "CI_07a_Base": "C_B_Dp100kB Taux mortalité maternelle",
        "CI_07b_Norm": "C_N_Dp100kB Taux mortalité enfant",
        "CI_07b_Base": "C_B_Dp100kB Taux mortalité enfant"

    })
    df.describe()
    return (df,)


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    # Récupération de l'année la plus récente pour l'analyse spatiale (ex: 2025)
    latestyear = df['Year'].max()
    df_latestyear = df[df['Year'] == latestyear]

    print(f"Nombre de lignes: {len(df)}. Année récente utilisée pour la cartographie : {df_latestyear}")
    return df_latestyear, latestyear


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data analysis
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    import glob
    import os
    import warnings

    # Paramètres de style pour des graphiques esthétiques et professionnels
    warnings.filterwarnings('ignore')
    sns.set_theme(style="whitegrid", palette="Set2")
    plt.rcParams['figure.figsize'] = (14, 7)
    plt.rcParams['font.size'] = 12
    return glob, plt, px, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Cartographie Mondiale et Distribution Spatiale
    Une vision globale permet immédiatement d'identifier les zones géographiques les plus exposées et les plus vulnérables.
    """)
    return


@app.cell
def _(df_latestyear, latestyear, px):
    fig1 = px.choropleth(
        df_latestyear, 
        locations="Code", 
        color="Risque global", 
        hover_name="Pays", 
        color_continuous_scale="Reds",
        title=f"Risque par continent ({latestyear})",
        labels={'Risque global': 'Risque'}
    )
    fig1.update_layout(geo=dict(showcoastlines=True), margin={"r":0,"t":40,"l":0,"b":0})
    fig1.show()
    return


@app.cell
def _(df_latestyear, latestyear, px):
    fig2 = px.choropleth(
        df_latestyear, 
        locations="Code", 
        color="Risque global", 
        hover_name="Pays", 
        color_continuous_scale="Purples",
        title=f"Vulnerabilité par continent ({latestyear})",
        labels={'Risque global': 'Vulnerabilité'}
    )
    fig2.update_layout(geo=dict(showcoastlines=True), margin={"r":0,"t":40,"l":0,"b":0})
    fig2.show()
    return


@app.cell
def _(df_latestyear, latestyear, px):
    fig3 = px.choropleth(
        df_latestyear, 
        locations="Code", 
        color="E_Exposition", 
        hover_name="Pays", 
        color_continuous_scale="Oranges",
        title=f"Exposition globale par continent ({latestyear})",
        labels={'E_Exposition': 'Exposition'}
    )
    fig3.update_layout(geo=dict(showcoastlines=True), margin={"r":0,"t":40,"l":0,"b":0})
    fig3.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Les Pays les Plus à Risque : Palmarès et Hiérarchies
    """)
    return


@app.cell
def _(df_latestyear, plt, sns):
    top_15_risk = df_latestyear.nlargest(15, 'Risque global')

    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_15_risk, x='Risque global', y='Pays', palette='Reds_r', edgecolor="black")
    plt.title('🔴 Top 15 pays par risque', fontsize=16, fontweight='bold')
    plt.xlabel('Risque')
    plt.ylabel('')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()
    return (top_15_risk,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Croisement : Exposition vs Vulnérabilité (Le Coeur du Risque)
    """)
    return


@app.cell
def _(df_latestyear, px):
    fig4 = px.scatter(
        df_latestyear, x='E_Exposition', y='V_Vulnérabilité', size='Risque global', color='Risque global', hover_name='Pays',
        color_continuous_scale='Turbo', size_max=40,
        labels={'E_Exposition': 'Exposition', 'V_Vulnérabilité': 'Vulnerabilité', 'Risque global': 'Global Risk'}
    )
    fig4.add_vline(x=df_latestyear['E_Exposition'].median(), line_dash="dash", line_color="gray", annotation_text="Exposition moyenne")
    fig4.add_hline(y=df_latestyear['V_Vulnérabilité'].median(), line_dash="dash", line_color="gray", annotation_text="Vulnerabilité moyenne")
    fig4.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig4.show()
    return


@app.cell
def _(df, plt, sns, top_15_risk):
    import matplotlib.ticker as ticker

    top_5_countries = top_15_risk.head(5)['Pays'].tolist()
    df_top_5 = df[df['Pays'].isin(top_5_countries)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_top_5, x='Year', y='V_Vulnérabilité', hue='Pays', marker='D', linewidth=2)
    plt.title('Tendance de vulnérabilité pour les 5 pays les plus à risque', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Vulnérabilité')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return (ticker,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Améliorations
    """)
    return


@app.cell
def _(df, plt, sns):
    min_year = df['Year'].min()
    max_year = df['Year'].max()

    df_start = df[df['Year'] == min_year][['Pays', 'Risque global', 'V_Vulnérabilité', 'C_Adaptation court-terme', 'Code']].set_index('Pays')
    df_end = df[df['Year'] == max_year][['Pays', 'Risque global', 'V_Vulnérabilité', 'C_Adaptation court-terme']].set_index('Pays')

    # Fusionner en calculant la différence Différence = Fin - Début 
    diff_df = df_end.join(df_start, lsuffix='_End', rsuffix='_Start').dropna()
    diff_df['Diff_V'] = diff_df['V_Vulnérabilité_End'] - diff_df['V_Vulnérabilité_Start']
    diff_df['Diff_Risque'] = diff_df['Risque global_End'] - diff_df['Risque global_Start']

    diff_df = diff_df.reset_index()

    # 1. Les 10 qui ont le plus baissé leur vulnérabilité (Amélioration !)
    top_improvers = diff_df.sort_values(by='Diff_V', ascending=True).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_improvers, x='Diff_V', y='Pays', palette='Greens_r')
    plt.title(f'Top 10 pays s\'étant amélioré ({min_year} -> {max_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Vulnérabilité')
    plt.ylabel('')
    plt.show()
    return diff_df, max_year, min_year


@app.cell
def _(diff_df, max_year, min_year, plt, sns):
    top_degraders = diff_df.sort_values(by='Diff_V', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_degraders, x='Diff_V', y='Pays', palette='Reds_r')
    plt.title(f'Top 10 pays s\'étant détérioré ({min_year} -> {max_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Vulnérabilité')
    plt.ylabel('')
    plt.show()
    return


@app.cell
def _(df, plt, sns, ticker):
    vuln_variance = df.groupby('Pays')['V_Vulnérabilité'].std().sort_values(ascending=False)
    top_5_var_v = vuln_variance.head(5).index.tolist()

    df_var_v = df[df['Pays'].isin(top_5_var_v)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_var_v, x='Year', y='V_Vulnérabilité', hue='Pays', marker='o', linewidth=2.5)
    plt.title('Évolution de la vulnérabilité parmi les plus fortes variations (2000-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Score de Vulnérabilité')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(sorted(df['Year'].dropna().unique()), rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return


@app.cell
def _(df, plt, sns, ticker):
    risk_variance = df.groupby('Pays')['Risque global'].std().sort_values(ascending=False)
    top_5_var_w = risk_variance.head(5).index.tolist()

    df_var_w = df[df['Pays'].isin(top_5_var_w)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_var_w, x='Year', y='Risque global', hue='Pays', marker='s', linewidth=2.5, palette='tab10')
    plt.title('Évolution du risque parmi les plus fortes variations (2000-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Score de risque')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(sorted(df['Year'].dropna().unique()), rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return


@app.cell
def _(df, plt, sns, ticker):
    exposure_variance = df.groupby('Pays')['E_Exposition'].std().sort_values(ascending=False)
    top_5_var_e = exposure_variance.head(5).index.tolist()

    df_var_e = df[df['Pays'].isin(top_5_var_e)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_var_e, x='Year', y='E_Exposition', hue='Pays', marker='^', linewidth=2.5, palette='Dark2')
    plt.title('Évolution de l\'Exposition aux aléas naturels parmi les plus fortes variations (2000-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Score d\'exposition')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(sorted(df['Year'].dropna().unique()), rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return


@app.cell
def _(df, plt, sns, ticker):
    top_5_tsunami = df.groupby('Pays')['E_Tsunamis'].mean().sort_values(ascending=False).head(5).index.tolist()
    df_tsunami = df[df['Pays'].isin(top_5_tsunami)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_tsunami, x='Year', y='E_Tsunamis', hue='Pays', marker='v', linewidth=2.5, palette='Blues_r')
    plt.title('Évolution de l\'exposition aux tsunamis parmi les pays les plus exposés', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Score exposition tsunamis')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(sorted(df['Year'].dropna().unique()), rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return


@app.cell
def _(df, plt, sns, ticker):
    top_5_seisme = df.groupby('Pays')['E_Séismes'].mean().sort_values(ascending=False).head(5).index.tolist()
    df_seisme = df[df['Pays'].isin(top_5_seisme)].sort_values(by='Year')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_seisme, x='Year', y='E_Séismes', hue='Pays', marker='s', linewidth=2.5, palette='Oranges_r')
    plt.title('Évolution de l\'exposition aux séismes parmi les pays', fontsize=15, fontweight='bold')
    plt.xlabel('Année')
    plt.ylabel('Score exposition séismes')
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(sorted(df['Year'].dropna().unique()), rotation=45)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    return


@app.cell
def _(df):
    for x in df.columns:
        print(x)
    return


@app.cell
def _(df, plt, sns):
    df_countries_corruption = df.groupby('Pays')['C_B_Sc Contrôle corruption'].mean().reset_index()
    top_ten_countries_good = df_countries_corruption.sort_values(by='C_B_Sc Contrôle corruption', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_ten_countries_good, x='C_B_Sc Contrôle corruption', y='Pays', palette='Greens_r')
    plt.title(f'Top 10 Countries with corruption control (2025)', fontsize=14, fontweight='bold')
    plt.xlabel('Corruption Control Score')
    plt.ylabel('')
    plt.show()
    return (df_countries_corruption,)


@app.cell
def _(df_countries_corruption, plt, sns):
    top_ten_countries_bad = df_countries_corruption.sort_values(by='C_B_Sc Contrôle corruption', ascending=True).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_ten_countries_bad, x='C_B_Sc Contrôle corruption', y='Pays', palette='Reds_r')
    plt.title(f'Top 10 Countries with corruption control (2025)', fontsize=14, fontweight='bold')
    plt.xlabel('Corruption Control Score')
    plt.ylabel('')
    plt.show()
    return


@app.cell
def _(df, sns):
    columns_to_corr = ['C_B_Sc Contrôle corruption', 'Risque global', 'S_Durée de vie', 'S_Education', 'S_Revenu', 'S_Indépendance aides', 'S_Manque infrastructures', 'S_Manque énergie', 'S_Manque IT', 'S_Manque agriculture', 'S_Disparités économiques', 'S_Disparités démographiques', 'S_Disparités genres', 'S_Touchés par épidémies et maladies', 'C_Personnel médical', 'C_Structures médicales']
    df_countries_scores_corr = df.groupby('Pays')[columns_to_corr].mean().reset_index()
    df_temp2 = df_countries_scores_corr[columns_to_corr].corr()
    X = df_temp2[['Risque global']]
    X.drop('Risque global', axis=0, inplace=True)
    sns.heatmap(X, annot=True, cmap='coolwarm', linewidths=0.5)
    return


@app.cell
def _(df, plt, sns):
    df_countries_healthcare = df.groupby('Pays')[['C_Personnel médical', 'C_Structures médicales']].mean().reset_index()
    df_countries_healthcare["avg"] = df_countries_healthcare[['C_Personnel médical', 'C_Structures médicales']].mean(axis=1)
    top_ten_countries2 = df_countries_healthcare.sort_values(by='avg', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_ten_countries2, x='avg', y='Pays', palette='Reds_r')
    plt.title(f'Top 10 Countries with healthcare access (2025)', fontsize=14, fontweight='bold')
    plt.xlabel('Healthcare Access Score')
    plt.ylabel('')
    plt.show()
    return


@app.cell
def _(df, plt, sns):
    df_countries_healthcare2 = df.groupby('Pays')[['C_Personnel médical', 'C_Structures médicales']].mean().reset_index()
    df_countries_healthcare2["avg"] = df_countries_healthcare2[['C_Personnel médical', 'C_Structures médicales']].mean(axis=1)
    top_ten_countries3 = df_countries_healthcare2.sort_values(by='avg', ascending=True).head(10).sort_values(by='avg', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_ten_countries3, x='avg', y='Pays', palette='Greens_r')
    plt.title(f'Top 10 Countries with healthcare access (2025)', fontsize=14, fontweight='bold')
    plt.xlabel('Healthcare Access Score')
    plt.ylabel('')
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
