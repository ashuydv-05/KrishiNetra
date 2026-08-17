#!/bin/bash

echo "===================================="
echo "Starting Sensor + YOLO in Parallel"
echo "===================================="

cd /home/tanay/final_7pm || exit

# Run sensor script in background
python3 combined_hardware_code.py &
SENSOR_PID=$!

# Run YOLO script in background
python3 yolo_L8.py &
YOLO_PID=$!

echo "Sensor PID: $SENSOR_PID"
echo "YOLO PID: $YOLO_PID"

# Stop both when Ctrl+C is pressed
trap "echo 'Stopping programs...'; kill $SENSOR_PID $YOLO_PID; exit" INT

wait

echo "===================================="
echo "Execution Finished"
echo "===================================="rname/final_7pm 
