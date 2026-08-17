# KrishiNetro

<p align="center">
  <strong>AI Based Crop Disease Detection and Edge Deployment System</strong>
</p>

<p align="center">
  An integrated system combining computer vision, edge AI, embedded systems, and hardware automation for crop disease detection.
</p>

---

## Overview

KrishiNetro is an AI based crop disease detection system that has been developed to perform disease identification on an NVIDIA Jetson device.

The system is using a YOLO based computer vision model for disease detection and has been integrated with GPIO based triggering, TensorRT optimized inference, UART communication, and an ESP32 for hardware interaction.

The system has been designed so that image processing and inference are being performed locally on the edge device. A physical push button is being used to initiate the detection process, after which the prediction is being processed and communicated to the ESP32.

### Key Components

| Component | Purpose |
|:---|:---|
| YOLO | Crop disease detection |
| NVIDIA Jetson | Edge inference and system execution |
| TensorRT | Model optimization and inference |
| GPIO | Physical trigger for detection |
| ESP32 | Hardware interaction |
| UART | Jetson to ESP32 communication |
| Shell Script | Application execution |
| systemd | Automated application startup |

The integration of these components has allowed the AI model to be connected with the physical hardware instead of being operated only through a manually executed prediction script.

---

## System Architecture

The system is centered around the NVIDIA Jetson, which is handling AI inference and communication with the hardware components.

A physical push button is connected to the Jetson through GPIO. When the button is pressed, the detection process is being triggered. The input is then being processed by the YOLO model, and the resulting prediction is being communicated to the ESP32 through UART.

~~~text
                         KRISHINETRO
                              |
                              v
                    +-------------------+
                    |   Physical Input  |
                    |    Push Button    |
                    +---------+---------+
                              |
                             GPIO
                              |
                              v
                    +-------------------+
                    |   NVIDIA Jetson   |
                    |                   |
                    |  Edge Processing  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   YOLO Detection  |
                    |                   |
                    | TensorRT Inference|
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Disease Prediction|
                    +---------+---------+
                              |
                             UART
                              |
                              v
                    +-------------------+
                    |       ESP32       |
                    |                   |
                    | Hardware Control  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Hardware Response |
                    +-------------------+
~~~

---

## End to End Workflow

The implemented workflow is following this sequence:

~~~text
System Start
     |
     v
Deployment Service
     |
     v
Application Initialization
     |
     v
Waiting for Hardware Trigger
     |
     v
GPIO Event Detected
     |
     v
Detection Process Started
     |
     v
Image Processing
     |
     v
YOLO Detection
     |
     v
TensorRT Optimized Inference
     |
     v
Disease Prediction
     |
     v
UART Communication
     |
     v
ESP32
     |
     v
Hardware Response
~~~

The hardware trigger is making the interaction event driven. The system is remaining in a waiting state until a GPIO event is detected, after which the inference pipeline is being initiated.

---

# AI Pipeline

## Dataset

The project has been using a dedicated dataset for developing the crop disease detection model.

The dataset preparation process has included the organization and preparation of crop disease images for model training.

The broader system also contains sensor and disease related data that has been used as part of the project.

The dataset has been prepared to provide the model with representative crop images for learning the visual characteristics associated with the target disease classes.

---

## YOLO Model Training

The disease detection model is based on the YOLO object detection framework.

The model has been trained using the prepared crop disease dataset and has been evaluated before being prepared for deployment.

The model development process has included:

1. Dataset preparation
2. Data annotation
3. Model training
4. Model evaluation
5. Model export
6. Deployment optimization

The training implementation is being maintained separately from the inference pipeline so that model development and deployment can be handled independently.

---

## Model Export and Optimization

The trained YOLO model has been converted through multiple formats for deployment.

~~~text
Trained YOLO Model
        |
        v
      LR8n.pt
        |
        v
     LR8n.onnx
        |
        v
 TensorRT Conversion
        |
        v
   LR8n.engine
        |
        v
Jetson Edge Inference
~~~

### Model Formats

| File | Purpose |
|:---|:---|
| `LR8n.pt` | Trained YOLO model |
| `LR8n.onnx` | Exported ONNX model |
| `LR8n.engine` | TensorRT inference engine |

The `.pt` model is representing the trained model. It has been exported to ONNX, and the ONNX model has then been converted into a TensorRT engine for deployment.

---

# Edge Deployment

## NVIDIA Jetson

Inference is being performed locally on the NVIDIA Jetson.

Instead of sending every image to a remote server, the system is processing the input locally on the edge device.

### Conventional Cloud Based Approach

~~~text
Input
  |
  v
Network
  |
  v
Remote Server
  |
  v
Inference
  |
  v
Result
~~~

### KrishiNetro Approach

~~~text
Input
  |
  v
NVIDIA Jetson
  |
  v
TensorRT Inference
  |
  v
Disease Prediction
~~~

This approach has reduced the dependency on continuous network connectivity and has kept the AI processing close to the physical system.

---

## TensorRT Optimization

The trained model has been converted into a TensorRT engine for inference on the NVIDIA Jetson.

TensorRT has been used to optimize the inference process for NVIDIA hardware.

~~~text
Trained YOLO Model
        |
        v
       ONNX
        |
        v
     TensorRT
        |
        v
 TensorRT Engine
        |
        v
Jetson Inference
~~~

The TensorRT engine is being used as the deployment oriented inference model.

Performance metrics such as inference latency, FPS, and the TensorRT precision mode can be added once the final measured values have been documented.

---

# Hardware Integration

## GPIO Based Trigger

A physical push button has been integrated with the NVIDIA Jetson through GPIO.

The button is being used to initiate the disease detection process.

~~~text
Push Button
     |
     v
   GPIO
     |
     v
Detection Trigger
     |
     v
AI Inference
~~~

The system is therefore not requiring the user to manually execute the prediction process every time a new detection is required.

The GPIO trigger has provided a simple physical interface between the user and the deployed AI system.

---

## Jetson and ESP32 Communication

The NVIDIA Jetson and ESP32 have been connected using UART communication.

The Jetson is handling the computationally intensive AI inference, while the ESP32 is handling the microcontroller side of the system.

After a prediction has been generated, the relevant information is being transmitted from the Jetson to the ESP32 through UART.

~~~text
+------------------------+
|      NVIDIA Jetson     |
|                        |
| YOLO + TensorRT        |
|          |             |
|          v             |
| Disease Prediction     |
+-----------+------------+
            |
           UART
            |
            v
+------------------------+
|         ESP32          |
|                        |
| Receive Prediction     |
|          |             |
|          v             |
| Hardware Operation     |
+------------------------+
~~~

This separation has allowed the Jetson to handle AI computation while the ESP32 is being used for hardware level operations.

---

# Automated Deployment

The deployment has been automated using a shell script and a systemd service.

The deployment process has been designed so that the required application can be started automatically when the Jetson is initialized.

~~~text
Jetson Startup
      |
      v
systemd Service
      |
      v
run_parallel.service
      |
      v
run_parallel.sh
      |
      v
Application Initialization
      |
      v
Waiting for GPIO Trigger
~~~

The systemd service is handling application startup, while the shell script is being used to coordinate the required execution processes.

This has removed the need to manually start the complete application after every system restart.

---

# Event Driven Operation

The hardware interaction is following an event driven execution model.

The system is remaining in a waiting state until a GPIO event is detected. When the physical button is pressed, the event is being detected and the inference process is being initiated.

~~~text
System Running
      |
      v
Waiting for Event
      |
      v
GPIO Event
      |
      v
Inference Started
      |
      v
Prediction Generated
      |
      v
Result Sent to ESP32
~~~

This approach is suitable for the current system because continuous inference is not required while the system is waiting for a new crop sample.

---

# Software and Hardware Integration

The project has integrated multiple software and hardware components into a single workflow.

| Layer | Component | Responsibility |
|:---|:---|:---|
| AI | YOLO | Disease detection |
| Optimization | TensorRT | Optimized inference |
| Edge Computing | NVIDIA Jetson | AI processing |
| Input | GPIO | Physical trigger |
| Communication | UART | Jetson to ESP32 communication |
| Hardware | ESP32 | Microcontroller operations |
| Automation | Shell Script | Process coordination |
| Startup | systemd | Automatic application startup |

The complete interaction is:

~~~text
Physical Input
      |
      v
GPIO
      |
      v
NVIDIA Jetson
      |
      v
AI Inference
      |
      v
Disease Prediction
      |
      v
UART
      |
      v
ESP32
      |
      v
Hardware Operation
~~~

The architecture has separated the computational workload from the hardware control workload. The Jetson is handling the AI inference, while the ESP32 is handling the microcontroller level operations.

---

# Technologies Used

| Category | Technology |
|:---|:---|
| Deep Learning | YOLO |
| Computer Vision | Object Detection |
| Model Export | ONNX |
| Inference Optimization | NVIDIA TensorRT |
| Edge Device | NVIDIA Jetson |
| Programming | Python |
| Hardware Trigger | GPIO |
| Microcontroller | ESP32 |
| Communication | UART |
| Automation | Shell Script |
| Service Management | systemd |
| Data | CSV |

---

# Key Implementation Areas

### AI and Computer Vision

The YOLO model has been trained for crop disease detection. The trained model has been exported and prepared for deployment.

The computer vision pipeline is responsible for processing the input and generating the disease prediction.

### Edge AI

Inference is being performed directly on the NVIDIA Jetson. TensorRT has been used to create an optimized inference engine for the target NVIDIA hardware.

This has allowed the trained model to be deployed locally instead of requiring a remote inference server.

### Embedded Systems

A physical push button has been connected through GPIO, and the Jetson has been connected to an ESP32 through UART.

The ESP32 is being used as the microcontroller interface for the hardware side of the system.

### Automation

The execution process has been automated using a shell script and a systemd service.

The system has been configured to initialize automatically and wait for the hardware trigger, allowing the complete workflow to be started without manually launching every component.

---

# Project Challenges

### Model Deployment on Edge Hardware

A model that has been trained successfully does not automatically provide efficient inference on an edge device.

The trained YOLO model has therefore been exported and converted into a TensorRT engine for deployment on the Jetson.

The deployment process has required the model to be prepared in a format that can be efficiently executed by the target NVIDIA hardware.

### AI and Hardware Integration

The project has required communication between the AI inference layer and the hardware layer.

GPIO is being used for the input event, while UART is being used to communicate the prediction to the ESP32.

The communication between these components has allowed the AI prediction to be passed from the Jetson to the hardware layer.

### Automated Execution

The complete application has been configured to start automatically rather than requiring every component to be launched manually.

The combination of systemd and shell scripting has been used to achieve this.

This has made the deployment process more consistent and has reduced the manual steps required to start the application.

---

# Results

The final measured results can be documented here.

| Metric | Value |
|:---|---:|
| Number of Classes | To be added |
| Dataset Size | To be added |
| Precision | To be added |
| Recall | To be added |
| mAP@50 | To be added |
| mAP@50:95 | To be added |
| Inference Latency | To be added |
| FPS | To be added |
| TensorRT Precision | To be added |

> **Note:** Only measured values should be added to this section.

The performance section will be updated with the actual training and deployment measurements once they have been verified.

---

# Future Scope

The system can be extended by adding more crop and disease classes and by improving the trained detection model.

Further optimization of the TensorRT inference pipeline can also be explored to improve inference performance on the edge device.

Additional environmental sensors can be integrated with the existing hardware system. Data logging and remote monitoring can be added for maintaining historical information about detected diseases.

The system can also be extended with a web or mobile interface for monitoring predictions and system status.

Further automation can be implemented so that detected crop conditions can be used to initiate appropriate agricultural actions.

---

# Conclusion

KrishiNetro has been developed as an integrated crop disease detection system in which the AI model, edge device, and hardware components are working together.

The project has covered the process from YOLO model training and model conversion to TensorRT based edge inference, GPIO based triggering, UART communication, ESP32 integration, and automated deployment.

The system is performing disease detection locally on the edge device, while the prediction is being connected to the hardware layer through the ESP32.

The project has therefore combined computer vision, edge computing, embedded systems, communication protocols, and deployment automation into a single working system.

---
