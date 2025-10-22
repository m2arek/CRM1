import geopandas as gpd
import pandas as pd

# === Chemins des fichiers ===
fichier_entreprises = "geo_siret_corse_commerciaux_merged.xlsx"
fichier_batiments_2a = "batiments_2A_toitures_sup500m2_polygones.geojson"
fichier_batiments_2b = "batiments_2B_toitures_sup500m2_polygones.geojson"

# === Charger les entreprises ===
df_entreprises = pd.read_excel(fichier_entreprises, dtype=str)

# Conversion en GeoDataFrame (points)
gdf_entreprises = gpd.GeoDataFrame(
    df_entreprises,
    geometry=gpd.points_from_xy(
        df_entreprises["longitude"].astype(float),
        df_entreprises["latitude"].astype(float)
    ),
    crs="EPSG:4326"
)

# === Charger les bâtiments ===
gdf_bat_2a = gpd.read_file(fichier_batiments_2a)
gdf_bat_2b = gpd.read_file(fichier_batiments_2b)

gdf_batiments = pd.concat([gdf_bat_2a, gdf_bat_2b], ignore_index=True)
gdf_batiments = gpd.GeoDataFrame(gdf_batiments, geometry="geometry", crs="EPSG:4326")

# Corriger les MultiPolygons en Polygons simples
gdf_batiments = gdf_batiments.explode(index_parts=False)

# === Jointure spatiale ===
gdf_join = gpd.sjoin(
    gdf_entreprises,
    gdf_batiments[["geometry", "surface_m2"]],
    how="left",
    predicate="within"
)

# === Export ===
fichier_sortie = "entreprises_batiments_surface.xlsx"
gdf_join.drop(columns="geometry").to_excel(fichier_sortie, index=False)

print(f"✅ Fichier généré : {fichier_sortie}")
