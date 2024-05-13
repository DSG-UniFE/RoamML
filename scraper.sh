#!/bin/bash

# Output file
output_file="perf_full.txt"

# extract the performance line from all the logs, stores in a temporary file
if [ ! -f "performance.tmp" ]; then
	for file in *.log; do
    		grep "performance with" "$file" >> performance.tmp
	done
fi

# sort for time and date, save the result and remove the temporary file
echo "--- Full performance ---"
sort -k1,1 performance.tmp | tee $output_file
rm performance.tmp

# Input log file
log_file="perf_full.txt"

# Output files
output_file_timestamp="perf_time_ordered.txt"
output_file_nod="perf_nod_ordered.txt"

# Extract nod and acc values, sort by timestamp and write to output_file_timestamp
echo ""
echo "--- Time ordered performance ---"
echo "date time nodID accuracy loss" | tee "tmp"
awk '{match($0, /nod[0-9]+/, nod); match($0, /acc=[0-9.]+/, acc); match($0, /loss=[0-9.]+/, loss); gsub(/\./, ",", acc[0]); gsub(/\./, ",", loss[0]); print $1, $2, nod[0], substr(acc[0], 5), substr(loss[0], 6)}' "$log_file" | sort -k1,2 | tee -a "tmp"

cp "tmp" $output_file_timestamp
cut -d " " -f 4 "tmp" >> $output_file_timestamp
cut -d " " -f 5 "tmp" >> $output_file_timestamp

# Extract nod and acc values, sort by nod and write to output_file_nod
echo ""
echo "--- Node id ordered performance ---"
echo "date time nodID accuracy loss" | tee "tmp"
awk '{match($0, /nod[0-9]+/, nod); match($0, /acc=[0-9.]+/, acc); match($0, /loss=[0-9.]+/, loss); gsub(/\./, ",", acc[0]); gsub(/\./, ",", loss[0]); print $1, $2, nod[0], substr(acc[0], 5), substr(loss[0], 6)}' "$log_file" | sort -k3 | tee -a "tmp"

cp "tmp" $output_file_nod
cut -d " " -f 4 "tmp" >> $output_file_nod
cut -d " " -f 5 "tmp" >> $output_file_nod

rm tmp

echo "Files created: $output_file_timestamp, $output_file_nod"

