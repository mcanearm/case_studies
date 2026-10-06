# claude generated
mkdir -p mi_parquet
while read -r id; do
  aws s3 cp --no-sign-request --recursive --quiet \
    "s3://noaa-ghcn-pds/parquet/by_station/STATION=$id/ELEMENT=PRCP/" "/tmp/ghcn/$id/"
  find "/tmp/ghcn/$id" -name '*.parquet' | while read -r f; do
    mv "$f" "mi_parquet/${id}_$(basename "$f")"
  done
done < MI_stations.txt
rm -rf /tmp/ghcn